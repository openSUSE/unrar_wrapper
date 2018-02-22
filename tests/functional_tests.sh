#!/bin/bash
#
# Perform basic functional testing of the unrar_wrapper

# Color definition
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # no color


#######################################
# Run command via UnRAR and unrar_wrapper
# and compare results.
# Globals:
#   WRAPPER
# Arguments:
#   command: command using UnRAR syntax
# Returns:
#   None  
#######################################
function run_test(){
  local command="$1"

  echo "------------------------------------------"
  echo "Tested command: ${command}"
  echo "------------------------------------------"
    
  # Set up
  local unrardir=$(mktemp -d)
  local wrapperdir=$(mktemp -d)
  
  # Run the test case for UnRAR and unrar_wrapper
  cd ${unrardir}
  unrar ${command} >/dev/null 2>&1
  local rc1=$?

  cd ${wrapperdir}
  ${WRAPPER} ${command} >/dev/null 2>&1
  local rc2=$?

  # Check return codes
  # if rc1=0 then rc2 must be 0, if rc1!=0 then rc2 must be 1 or 2
  local rcstatus=0
  if ([[ ${rc1} == 0 ]] && [[ ${rc2} -ne 0 ]]) || ([[ ${rc1} -ne 0 ]] && [[ ${rc2} == 0 ]]); then
    echo "Return code mismatch (UnRAR rc=${rc1}; unrar_wrapper rc=${rc2})"
    rcstatus=1
  fi

  # Check if the output is the same
  diff -r -q ${unrardir} ${wrapperdir}
  local diffstatus=$?
    
  # Evaluate
  # fail if directories or rc codes differ, warn if UnRAR reports that archive,
  # files or @listfiles don't exist
  if [[ ${diffstatus} == 0 ]] && [[ ${rcstatus} == 0 ]]; then
    echo -e "${GREEN}Test passed.${NC}"
  elif [[ ${rc1} == 6 ]] || [[ ${rc2} == 10 ]]; then
    echo -e "${YELLOW}Test files not found.${NC}"
  else
    echo -e "${RED}Test failed!${NC}"
  fi    

  # Tear down
  rm -rf ${unrardir}
  rm -rf ${wrapperdir}
  echo
}


function main() {
  if [[ $# -ne 2 ]]; then
    echo "usage: ./functional_tests.sh <path_to_test_datadir> <path_to_wrapper_script>"
    exit 1
  fi

  DATADIR=$(readlink -f $1)
  WRAPPER=$(readlink -f $2)

  TESTCASES_EXTRACT=(
    "k ${DATADIR}/empty_dir.rar" # non-existing command
    "x ${DATADIR}/nonexisting.rar" # non-existing archive
    "x ${DATADIR}/file_without_dir.rar"
    "x ${DATADIR}/files_without_dir.rar"
    "x ${DATADIR}/one_dir_one_file.rar"
    "x ${DATADIR}/empty_dir.rar"
    "x ${DATADIR}/many_dirs_no_file.rar"
    "x ${DATADIR}/many_dirs_many_files.rar"
    "x ${DATADIR}/many_dirs_many_files_pass.rar -pmypassword"
    "x ${DATADIR}/many_dirs_many_files.rar maindir/subdir2/b/anotherfile maindir/subdir4/fifth/fifth_file"
    "x ${DATADIR}/many_dirs_many_files.rar maindir/subdir2/b/*"
    "x ${DATADIR}/many_dirs_many_files.rar @${DATADIR}/listfiles1"
    "x ${DATADIR}/many_dirs_many_files.rar @${DATADIR}/listfiles2"
    "x ${DATADIR}/many_dirs_many_files.rar @${DATADIR}/listfiles1 @${DATADIR}/listfiles2"
    "x ${DATADIR}/many_dirs_many_files.rar @${DATADIR}/nonexisting" # non-existing list file
    "x ${DATADIR}/many_dirs_many_files.rar newdir/"
    "x ${DATADIR}/many_dirs_many_files.rar maindir/subdir2/b/anotherfile maindir/subdir4/fifth/fifth_file @${DATADIR}/listfiles1 @${DATADIR}/listfiles2 newdir/"
    "x ${DATADIR}/many_dirs_many_files.rar newdir/ @${DATADIR}/listfiles1 maindir/subdir2/b/anotherfile @${DATADIR}/listfiles2 maindir/subdir4/fifth/fifth_file"
  )

  for testcase in "${TESTCASES_EXTRACT[@]}"; do
    run_test "${testcase}"
  done
}

main "$@"
exit 0
