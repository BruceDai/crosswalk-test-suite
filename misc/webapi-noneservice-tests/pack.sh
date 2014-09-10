#!/bin/bash
source $(dirname $0)/webapi-noneservice-tests.spec

usage="Usage: ./pack.sh [-a <apk runtime arch: x86 | arm>]"

arch="x86"
while getopts a: o
do
    case "$o" in
    a) arch=$OPTARG;;
    *) echo "$usage"
       exit 1;;
    esac
done

SRC_ROOT=$(cd $(dirname $0);pwd)
BUILD_ROOT=/tmp/${name}_pack
BUILD_DEST=/tmp/${name}

# clean
function clean_workspace(){
    echo "cleaning workspace... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    rm -rf $BUILD_ROOT $BUILD_DEST
}

clean_workspace
mkdir -p $BUILD_ROOT $BUILD_DEST

# copy source code
rm -rf $SRC_ROOT/*.zip
cp -arf $SRC_ROOT/* $BUILD_ROOT/

for list in $LIST;do
    cp -ar $list $BUILD_ROOT/
done

## creat testlist.json ##
echo "[
    {\"category\": \"W3C\", \"tests\":
        [" > $BUILD_DEST/testlist.json
for suite in $LIST;do
    echo "\"`basename $suite`\"",
done | sort | sed '$s/,//' >>$BUILD_DEST/testlist.json
echo "        ]
    }
]" >>$BUILD_DEST/testlist.json


for suite in $LIST;do
    python $SRC_ROOT/../../tools/build/pack.py -t apk-aio -m embedded -a $arch -d $BUILD_DEST -s $SRC_ROOT/../../webapi/`basename $suite`
done

mkdir $BUILD_ROOT/apps
mv `find /tmp/webapi-noneservice-tests/ -name '*apk'` $BUILD_ROOT/apps

## creat apk ##
cd $BUILD_DEST
cat > entry.html << EOF
<!doctype html>
<head>
    <meta http-equiv="Refresh" content="1; url=index.html?testprefix=./">
</head>
EOF
cp -a $BUILD_ROOT/icon.png     $BUILD_DEST/
cp -a $BUILD_ROOT/webrunner/*     $BUILD_DEST/
#cp -a $BUILD_ROOT/testlist.json     $BUILD_DEST/

cp -ar $SRC_ROOT/../../tools/crosswalk $BUILD_ROOT/crosswalk
cd $BUILD_ROOT/crosswalk
python make_apk.py --package=org.xwalk.$appname --name=$appname --app-root=$BUILD_DEST --app-local-path=entry.html --icon=$BUILD_DEST/icon.png --mode=embedded --arch=$arch --enable-remote-debugging
if [ $? -ne 0 ];then
    echo "Create $name.apk fail.... >>>>>>>>>>>>>>>>>>>>>>>>>"
    clean_workspace
    exit 1
fi

## cp tests.xml and inst.sh ##
mkdir -p $BUILD_DEST/opt/$name
cp $BUILD_ROOT/inst.py $BUILD_DEST/opt/$name/inst.py
cp -a $BUILD_ROOT/apps $BUILD_DEST/opt/$name

for suite in `ls $BUILD_ROOT |grep "\-tests" |grep -v spec$`;do
    cp $BUILD_ROOT/$suite/tests.xml  $BUILD_DEST/opt/$name/$suite.tests.xml
    cp $BUILD_ROOT/$suite/tests.full.xml  $BUILD_DEST/opt/$name/$suite.tests.full.xml
    sed -i "s/<suite/<suite widget=\"$name\"/g" $BUILD_DEST/opt/$name/$suite.tests.xml
    sed -i "s/<suite/<suite widget=\"$name\"/g" $BUILD_DEST/opt/$name/$suite.tests.full.xml
    rm -rf $BUILD_DEST/opt/$suite
done

## creat zip package ##
mv $BUILD_ROOT/crosswalk/*.apk $BUILD_DEST/opt/$name/
if [ -f $BUILD_DEST/opt/$name/WebapiNoneserviceTests_$arch.apk ];then
    mv $BUILD_DEST/opt/$name/WebapiNoneserviceTests_$arch.apk $BUILD_DEST/opt/$name/webapi_noneservice_tests.apk
fi
cd $BUILD_DEST

zip -Drq $BUILD_DEST/$name-$version-$sub_version.apk.zip opt/
if [ $? -ne 0 ];then
    echo "Create zip package fail... >>>>>>>>>>>>>>>>>>>>>>>>>"
    clean_workspace
    exit 1
fi

# copy zip file
echo "copy package from workspace... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
cp -f $BUILD_DEST/$name-$version-$sub_version.apk.zip $SRC_ROOT/

# clean workspace
clean_workspace

# validate
echo "checking result... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
if [ -z "`ls $SRC_ROOT | grep "\.zip"`" ];then
    echo "------------------------------ FAILED to build $name packages --------------------------"
    exit 1
fi

echo "------------------------------ Done to build $name packages --------------------------"
cd $SRC_ROOT
ls *.zip 2>/dev/null
