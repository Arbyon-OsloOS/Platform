import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.0

Window {
    id: win
    width: 850
    height: 600
    visible: true
    property string accent: "#0075db"
    property string cwd: "/"
    property bool sidebarShown: true
    property bool sidebarExplicitlyShown: false
    property bool sidebarExplicitlyHidden: false
    property bool animating: false
    property string appName: title

    // button radius = 6
    flags: "CustomizeWindowHint"
    //flags: "FramelessWindowHint"
    color: "transparent"
    //color  = "#181818"
    //radius = 9
    DropShadow {
        anchors.fill: w
        horizontalOffset: 0
        verticalOffset: 30
        radius: 30
        samples: 17
        color: "#80000000"
        source: w
    }
    property O_wframe w: _O_w
    }
}
