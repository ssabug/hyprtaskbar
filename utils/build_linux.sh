programName="hyprtaskbar"
system="linux"
version=$(cat utils/VERSION)
buildDir="build"
distDir="dist"
venvDir="venv"
requirementsFilePath="utils/requirements.txt"
buildZip="y"
deleteBuildFiles="y"

pr="////////////////////////// "

patch() {
    echo "Patching done"
}

install() {

    if [ -d "${venvDir}" ]; then
        echo "${pr}VENV directory already created"
    else
        echo "${pr}Creating VENV"
        python -m venv venv 
    fi
    echo "${pr}Activating VENV"
    source venv/bin/activate
    echo "${pr}Installing libraries"
    pip install -r "${requirementsFilePath}"
}

cleanDirs() {
    rm -rf "${buildDir}/"
    rm -rf "${distDir}/"
}

deleteFiles() {

    if [ "${deleteBuildFiles}" = "y" ]; then
        cleanDirs
    fi

}

prepareBinary() {

    echo "${pr}Creating binary"
    
    python -O -m PyInstaller ${programName}.py

    echo "${pr}Copying program data & doc"

    dataDestDir="${distDir}/${programName}/data"
    mkdir -p "${dataDestDir}"
    #cp -R "data/"* "${dataDestDir}/"
    cp config.json "${distDir}/${programName}/"
    cp style.scss "${distDir}/${programName}/"
    cp utils/hypertaskbar.desktop "${distDir}/${programName}/"

    docDestDir="${distDir}/${programName}/doc"
    mkdir -p "${docDestDir}"
    cp -R "doc"/* "${docDestDir}/"
    cp "README.md" "${docDestDir}/"
    mv "${programName}.spec" "${docDestDir}/"

    if [ "${buildZip}" = "y" ]; then
        echo "${pr}Creating ZIP release package"
        cd "${distDir}"
        zip -r "${programName}_${version}_${system}.zip" "${programName}"
        mv "${programName}_${version}_${system}.zip" ../
        cd ..
    fi

    deleteFiles

    echo "${pr}Build terminated, if zip file not created, check errors in terminal"
}

install
cleanDirs
prepareBinary