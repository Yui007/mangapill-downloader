import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "../theme"
import "../components"

/**
 * SettingsScreen - Configuration options
 */
Item {
    id: root
    
    signal back()
    
    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spacingL
        
        // ==================== Header ====================
        
        RowLayout {
            Layout.fillWidth: true
            spacing: Theme.spacingM
            
            // Back button
            Rectangle {
                width: 44
                height: 44
                radius: Theme.radiusM
                color: backMouse.containsMouse ? Theme.bgCardHover : "transparent"
                border.color: Theme.borderLight
                border.width: 1
                
                Text {
                    anchors.centerIn: parent
                    text: "←"
                    font.pixelSize: 20
                    color: Theme.textPrimary
                }
                
                MouseArea {
                    id: backMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.back()
                }
            }
            
            Text {
                text: "⚙️ Settings"
                font.pixelSize: Theme.fontSizeTitle
                font.bold: true
                color: Theme.textPrimary
            }
            
            Item { Layout.fillWidth: true }
        }
        
        // ==================== Download Settings ====================
        
        GlassCard {
            Layout.fillWidth: true
            Layout.preferredHeight: 230
            hoverable: false
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: Theme.spacingL
                spacing: Theme.spacingM
                
                Text {
                    text: "📁 DOWNLOAD SETTINGS"
                    font.pixelSize: Theme.fontSizeLarge
                    font.bold: true
                    color: Theme.accentPrimary
                }
                
                // Output Directory
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: Theme.spacingXS
                    
                    Text {
                        text: "Output Directory"
                        font.pixelSize: Theme.fontSizeMedium
                        color: Theme.textSecondary
                    }
                    
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: Theme.spacingS
                        
                        Rectangle {
                            Layout.fillWidth: true
                            height: 40
                            radius: Theme.radiusS
                            color: Theme.bgPrimary
                            border.color: Theme.borderLight
                            
                            Text {
                                anchors.left: parent.left
                                anchors.leftMargin: Theme.spacingM
                                anchors.verticalCenter: parent.verticalCenter
                                text: bridge.outputDir
                                font.pixelSize: Theme.fontSizeMedium
                                color: Theme.textPrimary
                                elide: Text.ElideMiddle
                                width: parent.width - 20
                            }
                        }
                        
                        NeonButton {
                            text: "Browse"
                            implicitWidth: 80
                            onClicked: folderDialog.open()
                        }
                    }
                }
                
                // Default Format & Keep Images
                RowLayout {
                    Layout.fillWidth: true
                    spacing: Theme.spacingXXL
                    
                    // Default Format section
                    ColumnLayout {
                        Layout.alignment: Qt.AlignTop
                        spacing: Theme.spacingS
                        
                        Text {
                            text: "Default Format"
                            font.pixelSize: Theme.fontSizeMedium
                            color: Theme.textSecondary
                        }
                        
                        RowLayout {
                            spacing: Theme.spacingS
                            
                            Repeater {
                                model: ["images", "pdf", "cbz"]
                                
                                Rectangle {
                                    width: 75
                                    height: 36
                                    radius: Theme.radiusS
                                    color: bridge.outputFormat === modelData ? Theme.accentPrimary : Theme.bgCard
                                    border.color: bridge.outputFormat === modelData ? Theme.accentPrimary : Theme.borderLight
                                    border.width: 1
                                    
                                    Text {
                                        anchors.centerIn: parent
                                        text: modelData.toUpperCase()
                                        font.pixelSize: Theme.fontSizeMedium
                                        font.bold: true
                                        color: bridge.outputFormat === modelData ? Theme.bgPrimary : Theme.textPrimary
                                    }
                                    
                                    MouseArea {
                                        anchors.fill: parent
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: bridge.outputFormat = modelData
                                    }
                                    
                                    Behavior on color { ColorAnimation { duration: Theme.animFast } }
                                }
                            }
                        }
                    }
                    
                    // Spacer
                    Item { Layout.fillWidth: true }
                    
                    // Keep Images section
                    ColumnLayout {
                        Layout.alignment: Qt.AlignTop
                        spacing: Theme.spacingS
                        
                        Text {
                            text: "Keep Images After Convert"
                            font.pixelSize: Theme.fontSizeMedium
                            color: Theme.textSecondary
                        }
                        
                        ToggleSwitch {
                            id: keepImagesToggle
                            Component.onCompleted: checked = bridge.keepImages
                            onToggled: bridge.keepImages = checked
                        }
                    }
                }
            }
        }
        
        // ==================== Performance Settings ====================
        
        GlassCard {
            Layout.fillWidth: true
            Layout.preferredHeight: 200
            hoverable: false
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: Theme.spacingL
                spacing: Theme.spacingM
                
                Text {
                    text: "⚡ PERFORMANCE"
                    font.pixelSize: Theme.fontSizeLarge
                    font.bold: true
                    color: Theme.accentPrimary
                }
                
                GridLayout {
                    Layout.fillWidth: true
                    columns: 2
                    columnSpacing: Theme.spacingXL
                    rowSpacing: Theme.spacingM
                    
                    // Chapter Workers
                    ColumnLayout {
                        spacing: Theme.spacingXS
                        
                        RowLayout {
                            Text {
                                text: "Chapter Workers"
                                font.pixelSize: Theme.fontSizeMedium
                                color: Theme.textSecondary
                            }
                            Item { Layout.fillWidth: true }
                            Text {
                                text: bridge.maxChapterWorkers.toString()
                                font.pixelSize: Theme.fontSizeMedium
                                font.bold: true
                                color: Theme.accentPrimary
                            }
                        }
                        
                        CustomSlider {
                            Layout.fillWidth: true
                            from: 1
                            to: 10
                            stepSize: 1
                            value: bridge.maxChapterWorkers
                            onValueChanged: bridge.maxChapterWorkers = value
                        }
                    }
                    
                    // Image Workers
                    ColumnLayout {
                        spacing: Theme.spacingXS
                        
                        RowLayout {
                            Text {
                                text: "Image Workers"
                                font.pixelSize: Theme.fontSizeMedium
                                color: Theme.textSecondary
                            }
                            Item { Layout.fillWidth: true }
                            Text {
                                text: bridge.maxImageWorkers.toString()
                                font.pixelSize: Theme.fontSizeMedium
                                font.bold: true
                                color: Theme.accentPrimary
                            }
                        }
                        
                        CustomSlider {
                            Layout.fillWidth: true
                            from: 1
                            to: 20
                            stepSize: 1
                            value: bridge.maxImageWorkers
                            onValueChanged: bridge.maxImageWorkers = value
                        }
                    }
                    
                    // Retry Count
                    ColumnLayout {
                        spacing: Theme.spacingXS
                        
                        RowLayout {
                            Text {
                                text: "Retry Count"
                                font.pixelSize: Theme.fontSizeMedium
                                color: Theme.textSecondary
                            }
                            Item { Layout.fillWidth: true }
                            Text {
                                text: bridge.retryCount.toString()
                                font.pixelSize: Theme.fontSizeMedium
                                font.bold: true
                                color: Theme.accentPrimary
                            }
                        }
                        
                        CustomSlider {
                            Layout.fillWidth: true
                            from: 1
                            to: 10
                            stepSize: 1
                            value: bridge.retryCount
                            onValueChanged: bridge.retryCount = value
                        }
                    }
                    
                    // Retry Delay
                    ColumnLayout {
                        spacing: Theme.spacingXS
                        
                        RowLayout {
                            Text {
                                text: "Retry Delay"
                                font.pixelSize: Theme.fontSizeMedium
                                color: Theme.textSecondary
                            }
                            Item { Layout.fillWidth: true }
                            Text {
                                text: bridge.retryDelay.toFixed(1) + "s"
                                font.pixelSize: Theme.fontSizeMedium
                                font.bold: true
                                color: Theme.accentPrimary
                            }
                        }
                        
                        CustomSlider {
                            Layout.fillWidth: true
                            from: 0.5
                            to: 10
                            stepSize: 0.5
                            value: bridge.retryDelay
                            decimals: 1
                            suffix: "s"
                            onValueChanged: bridge.retryDelay = value
                        }
                    }
                }
            }
        }
        
        // Spacer
        Item { Layout.fillHeight: true }
        
        // ==================== Save Button ====================
        
        RowLayout {
            Layout.fillWidth: true
            spacing: Theme.spacingM
            
            Item { Layout.fillWidth: true }
            
            NeonButton {
                text: "💾 SAVE SETTINGS"
                accentColor: Theme.success
                
                onClicked: {
                    bridge.saveConfig()
                    saveSuccess.visible = true
                    saveTimer.start()
                }
            }
            
            Text {
                id: saveSuccess
                text: "✓ Saved!"
                font.pixelSize: Theme.fontSizeMedium
                color: Theme.success
                visible: false
                
                Timer {
                    id: saveTimer
                    interval: 2000
                    onTriggered: saveSuccess.visible = false
                }
            }
            
            Item { Layout.fillWidth: true }
        }
    }
    
    // Folder dialog
    FolderDialog {
        id: folderDialog
        title: "Select Download Directory"
        
        onAccepted: {
            bridge.outputDir = selectedFolder.toString().replace("file:///", "")
        }
    }
}
