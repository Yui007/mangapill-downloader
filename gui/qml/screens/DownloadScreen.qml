import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../theme"
import "../components"

/**
 * DownloadScreen - Shows download progress
 */
Item {
    id: root
    
    property var manga: null
    property var selectedChapters: []
    
    property int totalChapters: selectedChapters.length
    property int completedChapters: 0
    property int failedChapters: 0
    property bool isDownloading: false
    property string currentStatus: "Starting..."
    
    signal back()
    signal finished()
    
    // Chapter status tracking
    property var chapterStatuses: []  // [{title, status: "pending"|"downloading"|"done"|"failed"}]
    
    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spacingL
        
        // ==================== Header ====================
        
        RowLayout {
            Layout.fillWidth: true
            
            Text {
                text: "📥 Downloading..."
                font.pixelSize: Theme.fontSizeTitle
                font.bold: true
                color: Theme.textPrimary
            }
            
            Item { Layout.fillWidth: true }
            
            // Cancel button
            Rectangle {
                width: cancelText.width + 24
                height: 36
                radius: Theme.radiusM
                color: cancelMouse.containsMouse ? Theme.error : "transparent"
                border.color: Theme.error
                border.width: 1
                
                Text {
                    id: cancelText
                    anchors.centerIn: parent
                    text: "❌ Cancel"
                    font.pixelSize: Theme.fontSizeMedium
                    color: cancelMouse.containsMouse ? Theme.textPrimary : Theme.error
                }
                
                MouseArea {
                    id: cancelMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        bridge.cancelDownload()
                        root.back()
                    }
                }
            }
        }
        
        // ==================== Main Progress ====================
        
        GlassCard {
            Layout.fillWidth: true
            Layout.preferredHeight: 140
            hoverable: false
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: Theme.spacingL
                spacing: Theme.spacingM
                
                Text {
                    text: root.manga ? root.manga.title : "Unknown"
                    font.pixelSize: Theme.fontSizeXLarge
                    font.bold: true
                    color: Theme.textPrimary
                    elide: Text.ElideRight
                    Layout.fillWidth: true
                }
                
                ProgressBar {
                    Layout.fillWidth: true
                    value: root.totalChapters > 0 ? root.completedChapters / root.totalChapters : 0
                    label: "Overall Progress"
                }
                
                Text {
                    text: root.currentStatus
                    font.pixelSize: Theme.fontSizeMedium
                    color: Theme.textSecondary
                }
            }
        }
        
        // ==================== Chapter List ====================
        
        GlassCard {
            Layout.fillWidth: true
            Layout.fillHeight: true
            hoverable: false
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: Theme.spacingM
                spacing: Theme.spacingS
                
                Text {
                    text: "📚 Chapter Progress"
                    font.pixelSize: Theme.fontSizeLarge
                    font.bold: true
                    color: Theme.textPrimary
                }
                
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    
                    ColumnLayout {
                        width: parent.width
                        spacing: Theme.spacingS
                        
                        Repeater {
                            model: root.chapterStatuses
                            
                            Rectangle {
                                Layout.fillWidth: true
                                height: 48
                                radius: Theme.radiusS
                                color: Theme.bgCard
                                border.color: Theme.borderLight
                                
                                RowLayout {
                                    anchors.fill: parent
                                    anchors.margins: Theme.spacingS
                                    spacing: Theme.spacingM
                                    
                                    // Status icon
                                    Text {
                                        text: {
                                            switch(modelData.status) {
                                                case "done": return "✅"
                                                case "failed": return "❌"
                                                case "downloading": return "⏳"
                                                default: return "⏸️"
                                            }
                                        }
                                        font.pixelSize: 20
                                    }
                                    
                                    // Chapter title
                                    Text {
                                        text: modelData.title
                                        font.pixelSize: Theme.fontSizeMedium
                                        color: Theme.textPrimary
                                        Layout.fillWidth: true
                                        elide: Text.ElideRight
                                    }
                                    
                                    // Status text
                                    Text {
                                        text: {
                                            switch(modelData.status) {
                                                case "done": return "Done"
                                                case "failed": return "Failed"
                                                case "downloading": return "Downloading..."
                                                default: return "Pending"
                                            }
                                        }
                                        font.pixelSize: Theme.fontSizeSmall
                                        color: {
                                            switch(modelData.status) {
                                                case "done": return Theme.success
                                                case "failed": return Theme.error
                                                case "downloading": return Theme.accentPrimary
                                                default: return Theme.textMuted
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        // ==================== Summary (shown when complete) ====================
        
        GlassCard {
            Layout.fillWidth: true
            Layout.preferredHeight: 140
            hoverable: false
            visible: !root.isDownloading && (root.completedChapters > 0 || root.failedChapters > 0)
            
            Rectangle {
                anchors.fill: parent
                radius: parent.radius
                gradient: Gradient {
                    GradientStop { position: 0.0; color: Qt.rgba(Theme.success.r, Theme.success.g, Theme.success.b, 0.1) }
                    GradientStop { position: 1.0; color: "transparent" }
                }
            }
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: Theme.spacingL
                spacing: Theme.spacingXL
                
                // Celebration icon
                Text {
                    text: root.failedChapters === 0 ? "🎉" : "📊"
                    font.pixelSize: 48
                    
                    SequentialAnimation on scale {
                        running: root.failedChapters === 0
                        loops: 3
                        NumberAnimation { to: 1.2; duration: 200; easing.type: Easing.OutQuad }
                        NumberAnimation { to: 1.0; duration: 200; easing.type: Easing.InQuad }
                    }
                }
                
                // Status text
                ColumnLayout {
                    spacing: 4
                    Layout.fillWidth: true
                    
                    Text {
                        text: root.failedChapters === 0 ? "Download Complete!" : "Download Finished"
                        font.pixelSize: Theme.fontSizeXLarge
                        font.bold: true
                        color: root.failedChapters === 0 ? Theme.success : Theme.warning
                    }
                    
                    Text {
                        text: {
                            var msg = root.completedChapters + " chapter" + (root.completedChapters !== 1 ? "s" : "") + " downloaded successfully"
                            if (root.failedChapters > 0) {
                                msg += ", " + root.failedChapters + " failed"
                            }
                            return msg
                        }
                        font.pixelSize: Theme.fontSizeMedium
                        color: Theme.textSecondary
                    }
                }
                
                // Stats boxes
                Row {
                    spacing: Theme.spacingM
                    
                    // Success stat
                    Rectangle {
                        width: 80
                        height: 70
                        radius: Theme.radiusM
                        color: Qt.rgba(Theme.success.r, Theme.success.g, Theme.success.b, 0.2)
                        border.color: Theme.success
                        border.width: 2
                        
                        Column {
                            anchors.centerIn: parent
                            spacing: 2
                            
                            Text {
                                anchors.horizontalCenter: parent.horizontalCenter
                                text: root.completedChapters.toString()
                                font.pixelSize: 28
                                font.bold: true
                                color: Theme.success
                            }
                            
                            Text {
                                anchors.horizontalCenter: parent.horizontalCenter
                                text: "SUCCESS"
                                font.pixelSize: 10
                                font.bold: true
                                color: Theme.success
                            }
                        }
                    }
                    
                    // Failed stat (only if there are failures)
                    Rectangle {
                        width: 80
                        height: 70
                        radius: Theme.radiusM
                        color: Qt.rgba(Theme.error.r, Theme.error.g, Theme.error.b, 0.2)
                        border.color: Theme.error
                        border.width: 2
                        visible: root.failedChapters > 0
                        
                        Column {
                            anchors.centerIn: parent
                            spacing: 2
                            
                            Text {
                                anchors.horizontalCenter: parent.horizontalCenter
                                text: root.failedChapters.toString()
                                font.pixelSize: 28
                                font.bold: true
                                color: Theme.error
                            }
                            
                            Text {
                                anchors.horizontalCenter: parent.horizontalCenter
                                text: "FAILED"
                                font.pixelSize: 10
                                font.bold: true
                                color: Theme.error
                            }
                        }
                    }
                }
                
                // Download More button
                NeonButton {
                    text: "📥 Download More"
                    accentColor: Theme.accentPrimary
                    onClicked: root.finished()
                }
            }
        }
    }
    
    // ==================== Bridge Connections ====================
    
    Connections {
        target: bridge
        
        function onDownloadProgress(current, total, status) {
            root.currentStatus = status
        }
        
        function onDownloadChapterComplete(title, success) {
            // Update chapter status
            for (var i = 0; i < root.chapterStatuses.length; i++) {
                if (root.chapterStatuses[i].title === title) {
                    var updated = root.chapterStatuses.slice()
                    updated[i] = { title: title, status: success ? "done" : "failed" }
                    root.chapterStatuses = updated
                    break
                }
            }
            
            if (success) {
                root.completedChapters++
            } else {
                root.failedChapters++
            }
        }
        
        function onDownloadFinished(successful, failed) {
            root.isDownloading = false
            root.currentStatus = "Download complete!"
            root.completedChapters = successful
            root.failedChapters = failed
        }
    }
    
    Component.onCompleted: {
        // Initialize chapter statuses
        if (root.manga && root.selectedChapters.length > 0) {
            var statuses = []
            for (var i = 0; i < root.selectedChapters.length; i++) {
                var idx = root.selectedChapters[i]
                var ch = root.manga.chapters[idx]
                statuses.push({ title: ch.title, status: "pending" })
            }
            root.chapterStatuses = statuses
            
            // Start download
            root.isDownloading = true
            bridge.startDownload(root.manga, root.selectedChapters)
        }
    }
}
