BASE_DIR="${HOME}/dev/hyprtaskbar"
CURRENT_DIR="$(pwd)"
GIT_NAME="hyprtaskbar"
GIT_URL="https://github.com/ssabug/${GIT_NAME}"


if [ -n "$1" ]
then
    COMMIT_MSG="$1"

    echo "/////// MOVING TO PROJECT DIR ${BASE_DIR}"
    cd "${BASE_DIR}"

    init() {
        echo "/////// INIT PROJECT DIR ${BASE_DIR}"
        git init
        echo "/////// LINK TO REMOTE REPO"
        git remote add "${GIT_NAME}" "${GIT_URL}"
        echo "/////// PUSH TO MASTER BRANCH"
        git push --set-upstream "${GIT_NAME}" master
    }

    if test -d .git/; then
        echo "/////// .git folder exists, no need to init"
    else
        init
    fi
    

    echo "/////// ADDING ALL FILES"
    git add --all

    echo "/////// COMMITTING ..."
    git commit -am "${COMMIT_MSG}"

    echo "/////// PUSHING ..."
    git push

    echo "/////// coming back to ${CURRENT_DIR}"
    cd "${CURRENT_DIR}"
else
    echo "Error : no git commit text supplied as argument"
fi



