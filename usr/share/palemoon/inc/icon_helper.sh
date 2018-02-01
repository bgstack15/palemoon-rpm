#!/bin/sh
# file: icon_helper.sh
# call: icon_helper [ install | remove ]
# started: 2018-01-30 18:22 for palemoon rpm
# limitations: only for application icons for now...

{

thisapp=palemoon
action="${1:-remove}" # default is remove
test -z "${IH_INDIR}" && export IH_INDIR=/usr/share/palemoon/app
test -z "${IH_OUTDIR}" && export IH_OUTDIR=/usr/share/icons/hicolor
find "${IH_INDIR}" -regex '.*.png' ! -regex '.*\/extensions\/.*' | while read infile ;
do
   thisfilename="$( basename "${infile}" )"
   shortname="${thisfilename%%.*}"
   extension="${thisfilename##*.}"
   size="$( echo "${shortname}" |  tr -dc '[[:digit:]]' )"
   destdir="$( { find "${IH_OUTDIR}" -maxdepth 1 -type d -regex ".*${size}.*" ; echo "/tmp" ; } | head -n1 )/apps"
   destfile="${destdir}/${thisapp}.${extension}"

   case "${action}" in
      install)
         ! test -e "${destfile}" && ln -s "${infile}" "${destfile}"
         ;;
      *)
         test -L "${destfile}" && /bin/rm "${destfile}"
         ;;
   esac
done

} 2>/dev/null
