#!/bin/bash
source $(dirname $0)/webapi-service-tests.spec
SRC_ROOT=$(cd $(dirname $0);pwd)
BUILD_ROOT=/tmp/${name}-${path_flag}_pack
BUILD_DEST=/tmp/${name}-${path_flag}

usage="Usage: ./pack.sh [-t <package type: apk | cordova>] [-a <apk runtime arch: x86 | arm | x86_64 | arm64>] [-m <package mode: embedded | shared>] [-p <local | npm>]
[-t apk] option was set as default.
[-a x86] option was set as default.
[-m embedded] option was set as default.
[-p local] option was set as default.
"

dest_dir=$SRC_ROOT
pack_type="apk"
arch="x86"
pack_mode="embedded"
crosswalk_version=""
crosswalk_branch=""
plugin_location="local"
while getopts a:t:m:d:p: o
do
    case "$o" in
    a) arch=$OPTARG;;
    t) pack_type=$OPTARG;;
    m) pack_mode=$OPTARG;;
    d) dest_dir=$OPTARG;;
    p) plugin_location=$OPTARG;;
    *) echo "$usage"
       exit 1;;
    esac
done

main_version=$(cat ../../VERSION | awk 'NR==2')
for((i=1;i<=4;i++)) 
do
    crosswalk_version=$(echo $main_version|cut -d "\"" -f$i)
done

crosswalk_branch_tmp=$(cat ../../VERSION | awk 'NR==3')
for((i=1;i<=4;i++)) 
do
    crosswalk_branch=$(echo $crosswalk_branch_tmp|cut -d "\"" -f$i)
done

rm -rf $dest_dir/$name-$version-$sub_version.$pack_type.zip

# clean
function clean_workspace(){
    echo "cleaning workspace... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    rm -rf $BUILD_ROOT
    rm -rf $BUILD_DEST
}

echo "cleaning workspace... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
clean_workspace
mkdir -p $BUILD_ROOT $BUILD_DEST

if [ $pack_type == "cordova" ]; then
    for list in $LIST;do
        python $SRC_ROOT/../../tools/build/pack.py -t ${pack_type}-aio -m $pack_mode -a $arch -d $BUILD_DEST --sub-version $sub_version --pack-type $plugin_location -s $SRC_ROOT/../../webapi/$list

        if [ -d $BUILD_DEST/opt/$list/HOST_RESOURCES ]; then
            mkdir -p $BUILD_ROOT/opt/$name/opt/$list
            mv $BUILD_DEST/opt/$list/HOST_RESOURCES/* $BUILD_ROOT/opt/$name/opt/$list
        fi
    done
else
    for list in $LIST;do
        python $SRC_ROOT/../../tools/build/pack.py -t ${pack_type}-aio -m $pack_mode -a $arch -d $BUILD_DEST -s $SRC_ROOT/../../webapi/$list
        if [ -d $BUILD_DEST/opt/$list/HOST_RESOURCES ]; then
            mkdir -p $BUILD_ROOT/opt/$name/opt/$list
            mv $BUILD_DEST/opt/$list/HOST_RESOURCES/* $BUILD_ROOT/opt/$name/opt/$list
        fi
    done

fi

if [ -d $BUILD_ROOT/opt/$name/opt ]; then
    mkdir -p $BUILD_ROOT/opt/$name/apps
    mv `find $BUILD_DEST -name '*apk'` $BUILD_ROOT/opt/$name/apps
    cp -a $SRC_ROOT/../../tools/resources/bdd/bddrunner $BUILD_ROOT/opt/$name
    cp -a $SRC_ROOT/../../tools/resources/bdd/data.conf $BUILD_ROOT/opt/$name
    cp -a $SRC_ROOT/../../tools/resources/xsl/* $BUILD_ROOT/opt/$name
fi

## creat apk ##
cp -a $SRC_ROOT/icon.png     $BUILD_ROOT/

if [ $pack_type == "apk" ];then
    #cp -ar $SRC_ROOT/../../tools/crosswalk $BUILD_ROOT/crosswalk

    cd $BUILD_ROOT
    #python make_apk.py --package=org.xwalk.$appname --name=$appname --app-url=http://127.0.0.1:8080/index.html --icon=$BUILD_ROOT/icon.png --mode=$pack_mode --arch=$arch --enable-remote-debugging
    crosswalk-pkg --android=$pack_mode --crosswalk=$crosswalk_version --manifest=''\{\"name\":\"$appname\"\,\"xwalk_package_id\":\"org.xwalk."$appname"\",\"start_url\":\"http://127.0.0.1:8080/index.html\"\}'' -p android --targets=$arch $BUILD_DEST
elif [ $pack_type == "cordova" ];then
    cp -ar $SRC_ROOT/../../tools/cordova_plugins $BUILD_ROOT/cordova_plugins
    cd $BUILD_ROOT
    cordova create $appname org.xwalk.$appname $appname
    sed -i "s/<widget/<widget android-activityName=\"$appname\"/g" $BUILD_ROOT/$appname/config.xml
    sed -i "s/<\/widget>/    <allow-navigation href=\"*\" \/>\\n<\/widget>/g" $BUILD_ROOT/$appname/config.xml
    cd $BUILD_ROOT/$appname
    cordova platform add android
    for plugin in `ls $BUILD_ROOT/cordova_plugins`
    do
        if [ $plugin == "cordova-plugin-crosswalk-webview" ]; then
            version_cmd=""
            plugin_crosswalk_source=$BUILD_ROOT/cordova_plugins/$plugin
            if [ $crosswalk_branch == "beta" ]; then
                if [ $pack_mode == "shared" ]; then
                    version_cmd="--variable XWALK_VERSION="org.xwalk:xwalk_shared_library_beta:$crosswalk_version""
                else
                    version_cmd="--variable XWALK_VERSION="org.xwalk:xwalk_core_library_beta:$crosswalk_version""
                fi
            else
                version_cmd="--variable XWALK_VERSION="$crosswalk_version""
            fi
            if [ $plugin_location == 'npm' ]; then
               plugin_crosswalk_source="cordova-plugin-crosswalk-webview"
            fi
            echo $version_cmd
            echo $plugin_crosswalk_source
            cordova plugin add $plugin_crosswalk_source $version_cmd --variable XWALK_MODE="$pack_mode"
        else
            cordova plugin add $BUILD_ROOT/cordova_plugins/$plugin
        fi
    done

    cd $BUILD_ROOT/$appname/www
    cat > index.html << EOF
<!doctype html>
<head>
    <meta http-equiv="Refresh" content="1; url=http://127.0.0.1:8080/index.html">
</head>
EOF
    cd $BUILD_ROOT/$appname

    pack_arch_tmp="arm"
    if [ $arch != 'arm' ]; then
        if [ $arch == 'x86' ]; then
            pack_arch_tmp="x86"
        elif [ $arch == 'x86_64' ]; then
            pack_arch_tmp="x86 --xwalk64bit"
        elif [ $arch == 'arm64' ]; then
            pack_arch_tmp="arm --xwalk64bit"
        else
            echo "apk runtime arch can only be x86 or arm or x86_64 or arm64, now take arm as default.... >>>>>>>>>>>>>>>"
            exit 1
        fi
    fi

    cordova build android -- --gradleArg=-PcdvBuildArch=$pack_arch_tmp

fi

if [ $? -ne 0 ];then
    echo "Create $name.apk fail.... >>>>>>>>>>>>>>>>>>>>>>>>>"
    clean_workspace
    exit 1
fi

## cp tests.xml and inst.sh ##
mkdir -p $BUILD_ROOT/opt/$name
cp $SRC_ROOT/inst.py $BUILD_ROOT/opt/$name/inst.py

for list in $LIST;do
    suite=`basename $list`
    cp $SRC_ROOT/../../webapi/$list/tests.xml  $BUILD_ROOT/opt/$name/$suite.tests.xml
    sed -i "s/<suite/<suite widget=\"$name\"/g" $BUILD_ROOT/opt/$name/$suite.tests.xml
    cp $SRC_ROOT/../../webapi/$list/tests.full.xml  $BUILD_ROOT/opt/$name/$suite.tests.full.xml
    sed -i "s/<suite/<suite widget=\"$name\"/g" $BUILD_ROOT/opt/$name/$suite.tests.full.xml
done

## creat zip package ##
if [ $pack_type == "apk" ];then
    mv $BUILD_ROOT/*.apk $BUILD_ROOT/opt/$name/
    mv $BUILD_ROOT/opt/$name/org.xwalk.webapi_service_tests*.apk $BUILD_ROOT/opt/$name/$appname.apk
elif [ $pack_type == "cordova" ];then
    apk_name_arch="armv7"
    if [ $arch != 'arm' ]; then
        apk_name_arch=$arch
    fi

    dir_source=$BUILD_ROOT/$appname/platforms/android/build/outputs/apk
    apk_source1=$dir_source/$appname-$apk_name_arch-debug.apk
    apk_source2=$dir_source/android-$apk_name_arch-debug.apk
    apk_dest=$BUILD_ROOT/opt/$name/$appname.apk
    if [ -f $apk_source1 ];then
        mv $apk_source1 $apk_dest
    elif [ -f $apk_source2 ];then
        mv $apk_source2 $apk_dest
    else
        echo "Copy apk failed, " + $apk_source1 + " does not exist"
        clean_workspace
        exit 1
    fi
fi

cd $BUILD_ROOT
zip -Drq $BUILD_ROOT/$name-$version-$sub_version.$pack_type.zip opt/
if [ $? -ne 0 ];then
    echo "Create zip package fail... >>>>>>>>>>>>#>>>>>>>>>>>>>"
    clean_workspace
    exit 1
fi

# copy zip file
echo "copy package from workspace... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd $SRC_ROOT
mkdir -p $dest_dir
cp -f $BUILD_ROOT/$name-$version-$sub_version.$pack_type.zip $dest_dir

# clean workspace
clean_workspace

# validate
echo "checking result... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
if [ ! -f $dest_dir/$name-$version-$sub_version.$pack_type.zip ];then
    echo "------------------------------ FAILED to build $name packages --------------------------"
    exit 1
fi

echo "------------------------------ Done to build $name packages --------------------------"
cd $dest_dir
ls *.zip 2>/dev/null
