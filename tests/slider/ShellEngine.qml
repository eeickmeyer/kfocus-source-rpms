import QtQuick

QtObject {
    property string stdout: ""
    property string commandStr: ""
    property string lastCommand: ""
    property bool mockFailure: false

    function exec(command) {
        lastCommand = command;
        let result;
        if (mockFailure) {
            result = "Mock failure";
        } else if (command.includes("/kfocus-power-profile get")) {
            result = "balanced\n";
        } else {
            result = "";
        }
        Qt.callLater(function() {
            if (stdout === result) stdoutChanged();
            else stdout = result;
        });
    }

    function ignoreResult() {}
}
