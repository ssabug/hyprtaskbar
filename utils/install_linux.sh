programName="hyprtaskbar"
system="linux"
version="$(cat utils/VERSION)"
zipFileName="${programName}_${version}_${system}.zip"
programDestination="/usr/share/${programName}"
configDestination="${HOME}/.config/${programName}"

pr="////////////////////////// "


extract_release_zip(){
    if test -d "${programName}"; then
        rm -rf "${programName}/"
    fi

    echo "${pr}Unzipping release file ${zipFileName}"
    unzip ${zipFileName}

    if test -d "${programDestination}"; then
        sudo rm -rf "${programDestination}/"
    fi

    sudo mkdir -p "${programDestination}"
    sudo mv "${programName}/"* "${programDestination}/"
    rm -rf "${programName}/"
}

copy_user_data(){
    echo "${pr}Copying user data to ${configDestination}" 
    mkdir -p "${configDestination}"
    cp "${programDestination}/config.json" "${configDestination}"
    cp "${programDestination}/style.scss" "${configDestination}"

}

build_application_file(){
    echo "${pr}Copying ${programDestination}/${programName}.desktop to /usr/share/applications/"
    sudo mv "${programDestination}/${programName}.desktop" "/usr/share/applications/"
}

install() {
    echo "${pr}installing ${programName}"

    extract_release_zip
 
    copy_user_data

    build_application_file

    echo "${pr}setup finished"
}

install