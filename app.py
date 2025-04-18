import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json
from math import floor

try:
    with open('config.json', "r+", encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print("未检测到配置文件，已自动生成配置文件。")
    with open('config.json', "w+", encoding="utf-8") as f:
        config = {
            "ip": "http://YOUR_PANEL_IP",
            "apikey": "YOUR_API_KEY",
            "setToken": "YOUR_TOKEN",
            "server_port": "SERVER_PORT",
            "debug": True,
            "serverConfig": {
                "serverName": "YOUR_SERVER_NAME",
                "serverIP": "YOUR_SERVER_IP",
                "serverPORT": "25565"
            },
            "bulletinConfig": {
                "bulletinEnabled": False,
                "bulletinTitle": "BULLETIN_TITLE",
                "bulletinContents": [
                    "THE_FIRST_SENTENCE",
                    "THE_SECOND_SENTENCE"
                ]
            }
        }

HOMEPAGE = '''<StackPanel.Resources>
    <Style TargetType="ListItem">
        <Setter Property="Foreground" Value="{DynamicResource ColorBrush1}"/>
        <Setter Property="Margin" Value="0,4"/>
    </Style>
    <Style TargetType="List">
        <Setter Property="Foreground" Value="{DynamicResource ColorBrush3}"/>
        <Setter Property="Margin" Value="20,6,0,6"/>
        <Setter Property="MarkerStyle" Value="1"/>
        <Setter Property="Padding" Value="0"/>
    </Style>
    <Style TargetType="Paragraph">
        <Setter Property="LineHeight" Value="12"/>
        <Setter Property="TextIndent" Value="0"/>
        <Setter Property="Margin" Value="0,8"/>
    </Style>
    <Style TargetType="TextBlock">
        <Setter Property="TextWrapping" Value="Wrap"/>
        <Setter Property="HorizontalAlignment" Value="Left"/>
        <Setter Property="FontSize" Value="14"/>
        <Setter Property="Foreground" Value="{DynamicResource ColorBrush1}"/>
    </Style>
    <Style TargetType="FlowDocument">
        <Setter Property="FontFamily" Value="Microsoft YaHei UI"/>
        <Setter Property="FontSize" Value="14"/>
        <Setter Property="TextAlignment" Value="Left"/>
        <Setter Property="Foreground" Value="{DynamicResource ColorBrush1}"/>
    </Style>
    <Style TargetType="FlowDocumentScrollViewer">
        <Setter Property="IsSelectionEnabled" Value="False"/>
        <Setter Property="VerticalScrollBarVisibility" Value="Hidden"/>
        <Setter Property="Margin" Value="0"/>
    </Style>
    <sys:String x:Key="LaunchIcon">
    M512 97C282.8 97 97 282.8 97 512s185.8 415 415 415 415-185.8
    415-415S741.2 97 512 97z m-1 759c-190.5 0-345-154.5-345-345s154.5-345
    345-345 345 154.5 345 345-154.5 345-345 345z M442.1 408.2L621.9 512
    442.1 615.8V408.2m-59.9-113.9c-5.2 0-10 4.2-10 10v415.4c0 5.8 4.8 10
    10 10 1.7 0 3.4-0.4 5-1.4l359.7-207.7c6.7-3.8 6.7-13.5 0-17.3L387.1
    295.7c-1.6-1-3.3-1.4-4.9-1.4z</sys:String>
    <Style x:Key="Quote" TargetType="Section">
        <Setter Property="BorderThickness" Value="5,0,0,0"/>
        <Setter Property="BorderBrush" Value="{DynamicResource ColorBrush4}"/>
        <Setter Property="Padding" Value="10,0"/>
        <Setter Property="Margin" Value="0,12"/>
    </Style>
    <Style x:Key="typedQuote" BasedOn="{StaticResource Quote}" TargetType="Section">
        <Setter Property="Padding" Value="10,2"/>
    </Style>
    <Style x:Key="devnoteQuote" BasedOn="{StaticResource typedQuote}" TargetType="Section">
        <Setter Property="BorderBrush" Value="{StaticResource ColorBrush4}"/>
        <Setter Property="Background" Value="{StaticResource ColorBrush6}"/>
    </Style>
    <Style x:Key="H2" TargetType="Paragraph">
        <Setter Property="FontSize" Value="22"/>
        <Setter Property="Margin" Value="0,10,0,5"/>
        <Setter Property="FontWeight" Value="Bold"/>
        <Setter Property="Foreground" Value="{DynamicResource ColorBrush3}"/>
    </Style>
    <ControlTemplate  x:Key="Separator" TargetType="ContentControl">
        <Grid Margin="0,10">
            <Grid.ColumnDefinitions>
                <ColumnDefinition Width="1*" />
                <ColumnDefinition Width="100" />
                <ColumnDefinition Width="1*" />
            </Grid.ColumnDefinitions>
            <Line X1="0" X2="100" Stroke="{DynamicResource ColorBrush4}" StrokeThickness="1.5" HorizontalAlignment="Center" Stretch="Fill" Grid.Column="0" />
            <TextBlock Text="{TemplateBinding Content}" HorizontalAlignment="Center" FontSize="15" Foreground="{DynamicResource ColorBrush4}" Grid.Column="1" VerticalAlignment="Center" />
            <Line X1="0" X2="100" Stroke="{DynamicResource ColorBrush4}" StrokeThickness="1.5" HorizontalAlignment="Center" Stretch="Fill" Grid.Column="2" />
        </Grid>
    </ControlTemplate>
    <Style x:Key="H4" TargetType="Paragraph">
        <Setter Property="FontSize" Value="16"/>
        <Setter Property="Margin" Value="0,10,0,1"/>
        <Setter Property="FontWeight" Value="Bold"/>
        <Setter Property="Foreground" Value="{DynamicResource ColorBrush4}"/>
    </Style>
    <Style x:Key="Lp" TargetType="Paragraph">
        <Setter Property="LineHeight" Value="16"/>
        <Setter Property="TextIndent" Value="0"/>
    </Style>
    <sys:String x:Key="WikiIcon">
    M172.61,196.65h31a7.69,7.69,0,0,1,7.62,6.65l11.19,80.95c2.58,20.09,5.16,40.18,7.73,60.79h1c3.61-20.61,7.47-41,11.34-60.79l18.23-81.58a7.7,7.7,0,0,1,7.52-6h26.58a7.7,7.7,0,0,1,7.51,6l18.48,81.6c3.86,19.57,7.21,40.18,11.07,60.79h1.29c2.32-20.61,4.9-41,7.22-60.79l11.67-81a7.7,7.7,0,0,1,7.62-6.6h27.72a7.7,7.7,0,0,1,7.59,9L364.41,382.2a7.69,7.69,0,0,1-7.58,6.38H311.61a7.7,7.7,0,0,1-7.54-6.14l-16-77.33c-3.09-14.68-5.67-30.14-7.47-44.57h-1c-2.58,14.43-4.9,29.89-7.73,44.57L256.34,382.4a7.7,7.7,0,0,1-7.54,6.18H204.6a7.69,7.69,0,0,1-7.58-6.32L165,205.72A7.71,7.71,0,0,1,172.61,196.65ZM286.87,507.39,159.71,455.25v22.82L97.54,451.18v-23.3l-89-2,9.54-119.29H44.78V291.24L31.45,280.81V247l14.09-4.23L45,227.13,63.33,220V207.1l5.51-2v-16.2l15.65-4.93V167.63l24.06-11.81,1.65-21.95,4.94-1.72-2-1V95.6h13V89.45l27.56-14.79L169,84.43,185.79,76l21.47,15.34,8.1,1v7.91h6.51l60.65-30.56,8,3.49,17-12.08L324,71l.12-2.19,39.15-22,18.06,12.53h26.37l3.79-1.62,36.38,27.4v28.77l16.81,8.15V149l6.08,3V164l10.15,5.51v11.32h9v11.52l1,0c1.54,0,3.44.08,5.91,0l15.13-.13V212.7h9.28v49.71h-5.8v36.1l-16,9h56l6.78,119.85-116.84-1.4Zm-157.16-85.7h27.23l128.51,52.7,152.82-78.54,92.15,1.1-3.36-59.47H456.67V325.89h-5.8v-40l22.37,1.81L485.36,281v-.86h-7.24V268.5h-7V236.33l-11.31,8.61V210.82h-9V187.35l-10.15-5.51V170.59l-11.59-5.79V138.2l-38.25-18.53,26.95-17.27v-2.29l-10.59-8-24.49,10.41V89.37H371.9l-10.35-7.18-8.38,4.7-.6,11.32-22.31,11.61-21.4-12.9L294,107.45l-10.58-4.63L192,148.87V130.24h-6.67V119l-1-.12V121l-28.12,4v.58h-7.1L151.49,150l-5.17-.37.11,3.38-1.27.44,14.7,10.59-45.37,22.26V206l-15.65,4.93V226l-5.51,2v12.57l-17.6,6.81.61,17.43-12,3.61,10.46,8.18v1.59h11.6v24l43.44,34.42h-84l-4.8,60,86.54,1.93v32.93l2.17.94ZM476.3,232.41h5.58v-4.25Z
    </sys:String>
    <Style x:Key="VersionTitleBorder" TargetType="Border">
        <Setter Property="Margin" Value="0,-12,-1,-2"/>
        <Setter Property="Background" Value="{DynamicResource ColorBrush3}"/>
        <Setter Property="Width" Value="170"/>
        <Setter Property="Height" Value="30"/>
        <Setter Property="CornerRadius" Value="7"/>
        <Setter Property="BorderThickness" Value="0,0,0,2"/>
        <Setter Property="BorderBrush" Value="{DynamicResource ColorBrush2}"/>
    </Style>
    <Style x:Key="H3" TargetType="Paragraph">
        <Setter Property="FontSize" Value="18"/>
        <Setter Property="Margin" Value="0,10,0,3"/>
        <Setter Property="FontWeight" Value="Bold"/>
        <Setter Property="Foreground" Value="{DynamicResource ColorBrush4}"/>
    </Style>
    <sys:String x:Key="DownloadIcon">
    M802 664v146c0 7.7-6.3 14-14 14H236c-7.7
    0-14-6.3-14-14V664c0-5.5-4.5-10-10-10h-50c-5.5
    0-10 4.5-10 10v170c0 33.1 26.9 60 60 60h600c33.1
    0 60-26.9 60-60V664c0-5.5-4.5-10-10-10h-50c-5.5
    0-10 4.5-10 10z M547 163v449.5l173.6-173.6c13.7-13.7
    35.8-13.7 49.5 0 13.7 13.7 13.7 35.8 0 49.5L536.8
    721.7c-0.4 0.4-0.8 0.8-1.3 1.2-0.2 0.2-0.4 0.4-0.6
    0.5-0.2 0.2-0.4 0.4-0.7 0.6-0.3 0.2-0.5 0.4-0.8 0.6-0.2
    0.1-0.4 0.3-0.5 0.4l-0.9 0.6c-0.2 0.1-0.3 0.2-0.5 0.3-0.3
    0.2-0.6 0.4-1 0.6-0.2 0.1-0.3 0.2-0.5 0.3-0.3 0.2-0.6
    0.4-1 0.5-0.2 0.1-0.4 0.2-0.5 0.3-0.3 0.2-0.6 0.3-0.9
    0.5l-0.6 0.3c-0.3 0.1-0.6 0.3-0.8 0.4-0.2 0.1-0.5 0.2-0.7
    0.3-0.3 0.1-0.5 0.2-0.8 0.3l-0.9 0.3c-0.2 0.1-0.4 0.2-0.7
    0.2-0.3 0.1-0.6 0.2-1 0.3-0.2 0.1-0.4 0.1-0.6 0.2-0.4 0.1-0.7
    0.2-1.1 0.3-0.2 0-0.4 0.1-0.6 0.1-0.4 0.1-0.7 0.2-1.1 0.2-0.2
    0-0.4 0.1-0.6 0.1-0.4 0.1-0.7 0.1-1.1 0.2-0.2 0-0.4 0.1-0.7
    0.1-0.3 0-0.7 0.1-1 0.1-0.3 0-0.6 0-0.9 0.1-0.3 0-0.5 0-0.8
    0.1-1.2 0.1-2.3 0.1-3.5 0-0.3 0-0.5 0-0.8-0.1-0.3 0-0.6
    0-0.9-0.1-0.3 0-0.7-0.1-1-0.1-0.2 0-0.4-0.1-0.7-0.1-0.4-0.1-0.7-0.1-1.1-0.2-0.2
    0-0.4-0.1-0.6-0.1-0.4-0.1-0.7-0.2-1.1-0.2-0.2
    0-0.4-0.1-0.6-0.1-0.4-0.1-0.7-0.2-1.1-0.3-0.2-0.1-0.4-0.1-0.6-0.2-0.3-0.1-0.6-0.2-1-0.3-0.2-0.1-0.5-0.1-0.7-0.2l-0.9-0.3c-0.3-0.1-0.5-0.2-0.8-0.3-0.2-0.1-0.5-0.2-0.7-0.3-0.3-0.1-0.6-0.3-0.8-0.4l-0.6-0.3c-0.3-0.2-0.6-0.3-0.9-0.5-0.2-0.1-0.4-0.2-0.5-0.3-0.3-0.2-0.6-0.4-1-0.6-0.2-0.1-0.3-0.2-0.5-0.3-0.3-0.2-0.6-0.4-1-0.6-0.2-0.1-0.3-0.2-0.5-0.3-0.3-0.2-0.6-0.4-0.9-0.7-0.2-0.1-0.3-0.3-0.5-0.4-0.3-0.2-0.5-0.4-0.8-0.6-0.2-0.2-0.4-0.4-0.7-0.6-0.2-0.2-0.4-0.4-0.6-0.5l-1.2-1.2-233.1-233.1c-13.7-13.7-13.7-35.8 0-49.5 13.7-13.7
    35.8-13.7 49.5 0L477 612.5V163c0-19.3 15.7-35 35-35s35 15.7 35 35z</sys:String>
    <Style x:Key="Card" TargetType="local:MyCard">
        <Setter Property="Margin" Value="0,5"/>
    </Style>
    <Style TargetType="TextBox" x:Key="BlockCode">
        <Setter Property="Foreground" Value="{DynamicResource ColorBrush1}" />
        <Setter Property="FontSize" Value="14" />
        <Setter Property="IsReadOnly" Value="True" />
        <Setter Property="FontFamily" Value="Consolas" />
        <Setter Property="Template">
            <Setter.Value>
                <ControlTemplate TargetType="TextBox">
                    <Border Background="{DynamicResource ColorBrush7}" Opacity="0.8" BorderBrush="{DynamicResource ColorBrush4}" BorderThickness="0" CornerRadius="0,0,5,5" Padding="16,8,16,12">
                        <ScrollViewer x:Name="PART_ContentHost" Focusable="false" HorizontalScrollBarVisibility="Hidden" VerticalScrollBarVisibility="Hidden" />
                    </Border>
                </ControlTemplate>
            </Setter.Value>
        </Setter>
    </Style>
    <Style x:Key="InnerImage" TargetType="Image">
        <Setter Property="MaxHeight" Value="500"/>
        <Setter Property="HorizontalAlignment" Value="Center"/>
    </Style>
    <Style x:Key="ContentStack" TargetType="StackPanel">
        <Setter Property="Margin" Value="20,40,20,20"/>
    </Style>
    <Style x:Key="BlockCodeBorder" TargetType="Border">
        <Setter Property="Background" Value="{DynamicResource ColorBrush4}"/>
        <Setter Property="Opacity" Value="0.8"/>
        <Setter Property="CornerRadius" Value="5"/>
        <Setter Property="Margin" Value="2"/>
    </Style>
    <Style x:Key="VersionTitleBlock" TargetType="TextBlock">
        <Setter Property="HorizontalAlignment" Value="Center"/>
        <Setter Property="TextAlignment" Value="Center"/>
        <Setter Property="VerticalAlignment" Value="Center"/>
        <Setter Property="Foreground" Value="{DynamicResource ColorBrush7}"/>
        <Setter Property="Width" Value="180"/>
        <Setter Property="TextWrapping" Value="Wrap"/>
        <Setter Property="FontSize" Value="18"/>
    </Style>
    <Style x:Key="DownloadVersionButton" TargetType="local:MyIconTextButton">
        <Setter Property="Text" Value="下载"/>
        <Setter Property="ToolTip" Value="转到下载页面"/>
        <Setter Property="EventType" Value="切换页面"/>
        <Setter Property="EventData" Value="1|1"/>
    </Style>
    <Style x:Key="VersionImageBorder" TargetType="Border">
        <Setter Property="HorizontalAlignment" Value="Center"/>
        <Setter Property="BorderThickness" Value="4"/>
        <Setter Property="VerticalAlignment" Value="Top"/>
        <Setter Property="BorderBrush" Value="{DynamicResource ColorBrush3}"/>
        <Setter Property="CornerRadius" Value="7"/>
        <Setter Property="MaxHeight" Value="140"/>
    </Style>
    <Style x:Key="H5" TargetType="Paragraph">
        <Setter Property="FontSize" Value="14"/>
        <Setter Property="Margin" Value="0,8,0,1"/>
        <Setter Property="Foreground" Value="{DynamicResource ColorBrush4}"/>
    </Style>
    <Style x:Key="H1" TargetType="Paragraph">
        <Setter Property="FontSize" Value="24"/>
        <Setter Property="Margin" Value="0,10,0,10"/>
        <Setter Property="FontWeight" Value="Bold"/>
        <Setter Property="Foreground" Value="{DynamicResource ColorBrush3}"/>
    </Style>
    <sys:String x:Key="CloudIcon">
    M480 224c43 0 84.7 11.6 120.6 33.5 34.6 21.1 62.5 50.9 80.6 86 10.4
    20.1 30.6 33.3 53.2 34.6C796 381.6 853 407 895.2 449.7c41.7 42.1 64.6
    97.2 64.6 155 0 30.8-5.9 60.6-17.7 88.7-11.3 27.1-27.5 51.4-48.2 72.3-42.3
    42.8-98.4 66.3-158 66.3h-478c-53.3-3.1-102.6-24-139-58.8-35.3-33.6-54.7-77.2-54.7-122.5
    0-38.5 13.7-75.3 39.7-106.4 12.9-15.5 28.5-29.1 46.3-40.3 18.3-11.6
    38.4-20.4 59.9-26.3 26.1-7.1 44.9-29.9 47-56.9 4-52.9 28.6-102.1
    69.4-138.7C368.1 244.6 422.6 224 480 224m0-64c-139.2 0-255.2 94.9-281.9
    220.8-4.4 20.8-18.5 38.3-38.2 46.3C65.8 465.6 0.2 551.2 0.2 650.7 0.2 781.3
    113.4 888.6 256.1 896H736c158.9 0 287.9-130.5 287.9-291.3
    0-145.4-111.1-265.5-256.2-287.4-18.1-2.7-34.1-13-44.2-28.2C672.5
    211.6 582.7 160 480 160z</sys:String>
    <sys:String x:Key="CreeperIcon">
    M213.333333 128a85.333333 85.333333 0 0 0-85.333333 85.333333v597.333334a85.333333 85.333333 0 0 0 85.333333 85.333333h597.333334a85.333333 85.333333 0 0 0 85.333333-85.333333V213.333333a85.333333 85.333333 0 0 0-85.333333-85.333333H213.333333z m0 64h597.333334c11.754667 0 21.333333 9.578667 21.333333 21.333333v597.333334c0 11.754667-9.578667 21.333333-21.333333 21.333333H213.333333c-11.754667 0-21.333333-9.578667-21.333333-21.333333V213.333333c0-11.754667 9.578667-21.333333 21.333333-21.333333z m64 106.666667a21.333333 21.333333 0 0 0-21.333333 21.333333v128a21.333333 21.333333 0 0 0 21.333333 21.333333h149.333334v-149.333333a21.333333 21.333333 0 0 0-21.333334-21.333333h-128z m149.333334 170.666666v85.333334h-64a21.333333 21.333333 0 0 0-21.333334 21.333333v160a32 32 0 1 0 64 0V704h213.333334v32a32 32 0 1 0 64 0V576a21.333333 21.333333 0 0 0-21.333334-21.333333h-64v-85.333334h-170.666666z m170.666666 0h149.333334a21.333333 21.333333 0 0 0 21.333333-21.333333v-128a21.333333 21.333333 0 0 0-21.333333-21.333333h-128a21.333333 21.333333 0 0 0-21.333334 21.333333v149.333333z
    </sys:String>
    <Style x:Key="tipQuote" BasedOn="{StaticResource typedQuote}" TargetType="Section">
        <Setter Property="BorderBrush" Value="#44AA55"/>
        <Setter Property="Background" Value="#3344AA55"/>
    </Style>
    <Style TargetType="TextBox" x:Key="InlineCode">
        <Setter Property="FontSize" Value="14" />
        <Setter Property="IsReadOnly" Value="True" />
        <Setter Property="Margin" Value="2,0,2,-4" />
        <Setter Property="FontFamily" Value="Consolas" />
        <Setter Property="Foreground" Value="{DynamicResource ColorBrush1}" />
        <Setter Property="Height" Value="18" />
        <Setter Property="Template">
            <Setter.Value>
                <ControlTemplate TargetType="TextBox">
                    <Border Background="{DynamicResource ColorBrush6}" Opacity="0.9" BorderBrush="{DynamicResource ColorBrush4}" BorderThickness="0" CornerRadius="5" Padding="4,0.2">
                        <ScrollViewer x:Name="PART_ContentHost" Focusable="false" HorizontalScrollBarVisibility="Hidden" VerticalScrollBarVisibility="Hidden" />
                    </Border>
                    <ControlTemplate.Triggers>
                    </ControlTemplate.Triggers>
                </ControlTemplate>
            </Setter.Value>
        </Setter>
    </Style>
    <Style x:Key="ServerJarDownloadButton" TargetType="local:MyIconTextButton">
        <Setter Property="Text" Value="服务端"/>
        <Setter Property="ToolTip" Value="下载服务端"/>
        <Setter Property="EventType" Value="下载文件"/>
    </Style>

    <SolidColorBrush x:Key="IconBrush" Color="#4A90E2"/>

    <Style x:Key="AnimatedPathStyle" TargetType="Path">
        <Setter Property="RenderTransformOrigin" Value="0.5,0.5"/>
        <Setter Property="RenderTransform">
            <Setter.Value>
                <RotateTransform Angle="0"/>
            </Setter.Value>
        </Setter>
        <Style.Triggers>
            <EventTrigger RoutedEvent="MouseLeftButtonDown">
                <BeginStoryboard>
                    <Storyboard>
                        <DoubleAnimation
                            Storyboard.TargetProperty="(Path.RenderTransform).(RotateTransform.Angle)"
                            From="0" To="360" Duration="0:0:0.5"/>
                    </Storyboard>
                </BeginStoryboard>
            </EventTrigger>
        </Style.Triggers>
    </Style>
</StackPanel.Resources>
 
<local:MyCard Margin="0,0,0,0">
    <Border BorderBrush="{DynamicResource ColorBrush2}" Margin="-0.6" CornerRadius="5" BorderThickness="0,0,0,10">
        <StackPanel>
            <TextBlock Text="%(ServerName)s 服务器面板"
                HorizontalAlignment="Left" 
                FontSize="20" 
                FontFamily="Microsoft Yahei Ui"
                Margin="16,12,12,0"
                FontWeight="Bold"/>
            <TextBlock Text="使用 FrozenLink v0.1.5 版本创建"
                HorizontalAlignment="Left" 
                FontSize="16" 
                Margin="16,12,12,12"/>
            <TextBlock Text="请给 FrozenLink 点个 star"
                Foreground="{DynamicResource ColorBrush2}"
                HorizontalAlignment="Right" 
                FontSize="16" 
                Margin="12,-30,50,12"/>
            <local:MyIconButton 
                Margin="0,-32,15,10" 
                Width="15" 
                Height="15" 
                HorizontalAlignment="Right" 
                ToolTip="刷新" 
                EventType="刷新主页">
                <Path 
                    Stretch="Uniform"
                    Width="15" 
                    Height="15" 
                    Style="{StaticResource AnimatedPathStyle}"
                    Data="M960 416V192l-73.056 73.056a447.712 447.712 0 0 0-373.6-201.088C265.92 63.968 65.312 264.544 65.312 512S265.92 960.032 513.344 960.032a448.064 448.064 0 0 0 415.232-279.488 38.368 38.368 0 1 0-71.136-28.896 371.36 371.36 0 0 1-344.096 231.584C308.32 883.232 142.112 717.024 142.112 512S308.32 140.768 513.344 140.768c132.448 0 251.936 70.08 318.016 179.84L736 416h224z"             
                    Fill="{StaticResource IconBrush}"/>
            </local:MyIconButton>
        </StackPanel>
    </Border>
</local:MyCard>

%(ServerBulletin)s

<local:MyCard Title="" Margin="0,8,0,12">
    <Grid>
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="*"/>
            <ColumnDefinition Width="Auto"/>
        </Grid.ColumnDefinitions>
        <Grid.RowDefinitions>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        
            <TextBlock 
                Text="%(ServerName)s 服务器信息"
                FontSize="18"
                FontWeight="Bold"
                HorizontalAlignment="Left"
                VerticalAlignment="Top"
                Margin="18,16,0,15"
                Grid.Column="0"
                Grid.Row="0"/>

        <StackPanel Grid.Column="0" Grid.Row="1" Margin="0,20,0,0"> 
            <TextBlock 
                Text="服务器版本：%(ProtocolName)s"
                FontSize="18"
                FontWeight="Bold"
                HorizontalAlignment="Left"
                VerticalAlignment="Top"
                Margin="18,0,88,15"/>
            <TextBlock 
                Text="在线玩家：%(PlayerCountString)s"
                FontSize="18"
                FontWeight="Bold"
                HorizontalAlignment="Left"
                VerticalAlignment="Top"
                Margin="18,0,15,15"/>
        </StackPanel>
        
        <StackPanel Grid.Column="1" Grid.Row="1" VerticalAlignment="Center" Margin="0,12,12,0">
            <local:MyIconTextButton
                Text="加入服务器" 
                Margin="0,0,15,8" 
                EventType="启动游戏" 
                EventData="\current|%(ServerIP)s" 
                ToolTip="将会以当前版本加入 %(ServerIP)s" 
                LogoScale="0.9"
                Logo="{StaticResource LaunchIcon}"
                Height="32"
                Width="120"/>
            <local:MyIconTextButton
                Text="点击复制地址"
                Margin="0,0,15,0"
                EventType="复制文本" 
                EventData="%(ServerIP)s" 
                ToolTip="复制服务器地址"
                LogoScale="0.9"
                Logo="M4 2H2v12h2V4h10V2zm2 4h12v2H8v10H6zm4 4h12v12H10zm10 10v-8h-8v8z"
                Height="32"
                Width="120"/>
        </StackPanel>
    </Grid>
</local:MyCard>


<local:MyCard Title="仪表盘" Margin="0,0,0,15">
    <Grid Margin="15,0,15,15">
        <Grid.RowDefinitions>
            <RowDefinition Height="*"/> <!-- 第一行 -->
            <RowDefinition Height="*"/> <!-- 第二行 -->
        </Grid.RowDefinitions>
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="*"/> <!-- 第一列 -->
            <ColumnDefinition Width="15"/> <!-- 分隔列（可选） -->
            <ColumnDefinition Width="*"/> <!-- 第二列 -->
        </Grid.ColumnDefinitions>

        <!-- 左上区块 -->
        <Border Grid.Row="0" Grid.Column="0" Margin="0,35,0,0" BorderThickness="1" BorderBrush="#44000000" CornerRadius="5">
            <StackPanel>
                <TextBlock Text="实例运行状态" 
                    FontSize="16" 
                    Margin="15,15,15,0"
                    FontWeight="Bold"/>
                <TextBlock Text="正在运行数 / 全部实例总数" 
                    FontSize="10" 
                    Margin="16,5,5,0"
                    Foreground="#666666"
                    FontWeight="Bold"/>
                <TextBlock 
                    Text="%(RunningInstances)s / %(TotalInstances)s"
                    FontSize="30"
                    HorizontalAlignment="Center"
                    VerticalAlignment="Top"
                    Margin="0,15,0,15"/>
            </StackPanel>
        </Border>

        <!-- 右上区块 -->
        <Border Grid.Row="0" Grid.Column="2" Margin="0,35,0,0" BorderThickness="1" BorderBrush="#44000000" CornerRadius="5">
            <StackPanel>
                <TextBlock Text="节点在线数" 
                    FontSize="16" 
                    Margin="15,15,15,0"
                    FontWeight="Bold"/>
                <TextBlock Text="在线节点 / 总节点" 
                    FontSize="10" 
                    Margin="16,5,5,0"
                    Foreground="#666666"
                    FontWeight="Bold"/>
                <TextBlock 
                    Text="%(RunningNodes)s / %(TotalNodes)s"
                    FontSize="30"
                    HorizontalAlignment="Center"
                    VerticalAlignment="Top"
                    Margin="0,15,0,15"/>
            </StackPanel>
        </Border>

        <!-- 左下区块 -->
        <Border Grid.Row="1" Grid.Column="0" Margin="0,15,0,0" BorderThickness="1" BorderBrush="#44000000" CornerRadius="5">
            <StackPanel>
                <TextBlock Text="系统资源信息" 
                    FontSize="16" 
                    Margin="15,15,15,0"
                    FontWeight="Bold"/>
                <TextBlock Text="面板主机 CPU，RAM 使用率" 
                    FontSize="10" 
                    Margin="16,5,5,0"
                    Foreground="#666666"
                    FontWeight="Bold"/>
                <TextBlock 
                    Text="%(CPUUsage)s% %(RAMUsage)s%"
                    FontSize="30"
                    HorizontalAlignment="Center"
                    VerticalAlignment="Top"
                    Margin="0,15,0,15"/>
            </StackPanel>
        </Border>

        <!-- 右下区块 -->
        <Border Grid.Row="1" Grid.Column="2" Margin="0,15,0,0" BorderThickness="1" BorderBrush="#44000000" CornerRadius="5">
            <StackPanel>
                <TextBlock Text="面板登录次数" 
                    FontSize="16" 
                    Margin="15,15,15,0"
                    FontWeight="Bold"/>
                <TextBlock Text="登录失败次数 : 登录成功次数" 
                    FontSize="10" 
                    Margin="16,5,5,0"
                    Foreground="#666666"
                    FontWeight="Bold"/>
                <TextBlock 
                    Text="%(FailedLogin)s : %(TotalLogin)s"
                    FontSize="30"
                    HorizontalAlignment="Center"
                    VerticalAlignment="Top"
                    Margin="0,15,0,15"/>
            </StackPanel>
        </Border>
    </Grid>
</local:MyCard>

<local:MyCard Title="主节点：%(NodeName)s" Margin="0,0,0,15">
    <Grid Margin="15,0,15,15">
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="*"/> <!-- 第一列 -->
            <ColumnDefinition Width="15"/> <!-- 分隔列 -->
            <ColumnDefinition Width="*"/> <!-- 第二列 -->
        </Grid.ColumnDefinitions>

        <!-- 左侧区块 -->
        <Border Grid.Column="0" Margin="0,35,0,0" BorderThickness="1" BorderBrush="#44000000" CornerRadius="5">
            <StackPanel>
                <TextBlock 
                    Text="节点地址" 
                    FontSize="13" 
                    Margin="15,15,15,0"
                    FontWeight="Bold"/>
                <local:MyTextButton 
                    Text="%(NodeIP)s"
                    FontSize="35"
                    FontWeight="Bold"
                    HorizontalAlignment="Center"
                    VerticalAlignment="Top"
                    Margin="0,15,0,15"
                    EventType="复制文本"
                    EventData="%(NodeIP)s"
                    Foreground="#000000"/>
            </StackPanel>
        </Border>

        <!-- 右侧区块 -->
        <Border Grid.Column="2" Margin="0,35,0,0" BorderThickness="1" BorderBrush="#44000000" CornerRadius="5">
            <StackPanel>
                <TextBlock
                    Text="节点版本" 
                    FontSize="13" 
                    Margin="15,15,15,0"
                    FontWeight="Bold"/>
                <TextBlock 
                    Text="%(NodeVersion)s"
                    FontSize="15"
                    FontWeight="Bold"
                    HorizontalAlignment="Center"
                    VerticalAlignment="Top"
                    Margin="0,15,0,15"/>
            </StackPanel>
        </Border>
    </Grid>
</local:MyCard>

<StackPanel Orientation="Horizontal" HorizontalAlignment="Center" Margin="0,0,0,15">
    <local:MyTextButton Text="FrozenLink" EventType="打开网页" EventData="https://github.com/CreeperIsASpy/FrozenLink" FontSize="12" Foreground="#666666"/>
    <TextBlock Text=" By " Foreground="#666666" FontSize="12"/>
    <local:MyTextButton Text="CreeperIsASpy / 仿生猫梦见苦力怕" EventType="打开网页" EventData="https://github.com/CreeperIsASpy" FontSize="12" Foreground="#666666"/>
</StackPanel>
'''

BULLETIN = '''
<local:MyCard Margin="0,24,0,0" CornerRadius="10">
<Border BorderBrush="{DynamicResource ColorBrush2}" Margin="-0.6" CornerRadius="5" BorderThickness="8,8,8,10">
<StackPanel>
<Border Style="{StaticResource VersionTitleBorder}" VerticalAlignment="Top">
<TextBlock Style="{StaticResource VersionTitleBlock}" Text="%(BulletinTitle)s"/>
</Border>
<FlowDocumentScrollViewer>
<FlowDocument>
%(BulletinContent)s
</FlowDocument>
</FlowDocumentScrollViewer>
</StackPanel>
</Border>
</local:MyCard>
'''


class DataGetter:
    def __init__(self):
        self.url = f"{config['ip']}/api/overview?apikey={config['apikey']}"
        self.apiurl = \
            f"https://api.mcsrvstat.us/3/{config['serverConfig']['serverIP']}:{config['serverConfig']['serverPORT']}"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "X-Requested-With": "XMLHttpRequest"
        }
        data = json.loads(requests.get(self.url, headers=headers).text)

        content_text = re.sub(r"(?<!%)%(?!\()", "%%", HOMEPAGE)
        svinfo = self.get_server_info()
        meta = {'ServerName': config["serverConfig"]["serverName"],
                'ServerBulletin': self.get_bulletin(),
                'ProtocolName': svinfo['protocol']['name'],
                'PlayerCountString': f'{svinfo["players"]["online"]}/{svinfo["players"]["max"]}',
                'ServerIP': config["serverConfig"]["serverIP"],
                'RunningInstances': data['data']['remote'][0]['instance']['running'],
                'TotalInstances': data['data']['remote'][0]['instance']['total'],
                'RunningNodes': data['data']['remoteCount']['available'],
                'TotalNodes': data['data']['remoteCount']['total'],
                'CPUUsage': floor(data['data']['chart']['system'][3]['cpu']),
                'RAMUsage': floor(data['data']['chart']['system'][3]['mem']),
                'FailedLogin': data['data']['record']['loginFailed'],
                'TotalLogin': data['data']['record']['logined'],
                'NodeName': data['data']['remote'][0]['remarks'],
                'NodeIP': data['data']['remote'][0]['ip'],
                'NodeVersion': data['data']['remote'][0]['version']}
        content_text = content_text.replace("}", "}}").replace("{", "{{")
        self.homepage = (content_text % meta).replace("}}", "}").replace("{{", "{")
        self.write_into_file()

    def get_server_info(self):
        headers = {
            'User-Agent': 'PCL2-Home/1.0 (https://github.com/icellye/PCL2-home)',
            'Accept': 'application/json'
        }
        resp = requests.get(self.apiurl, headers=headers)
        return json.loads(resp.text)

    def print_nested_dict(self, d, indent=0):
        """递归打印嵌套字典，使用缩进增强可读性"""
        for key, value in d.items():
            # 打印当前键（带缩进）
            print(' ' * indent + f"{key}:", end=' ')

            # 处理嵌套字典或普通值
            if isinstance(value, dict):
                print()  # 换行后开始子字典
                self.print_nested_dict(value, indent + 4)  # 递归调用，增加缩进
            else:
                print(value)  # 直接打印非字典值

    def write_into_file(self):
        with open("app.xaml", "w+", encoding='utf-8') as f:
            f.write(self.homepage)

    def get_bulletin(self):
        if not config['bulletinConfig']['bulletinEnabled']:
            return ""
        title = config['bulletinConfig']['bulletinTitle']
        contents = '\n'.join(list(map(lambda sentence: f"<Paragraph>{sentence}</Paragraph>",
                                      config['bulletinConfig']['bulletinContents'])))
        meta = {
            "BulletinTitle": title,
            "BulletinContent": contents
        }
        output = re.sub(r"(?<!%)%(?!\()", "%%", BULLETIN)
        output = output.replace("}", "}}").replace("{", "{{")
        output = (output % meta).replace("}}", "}").replace("{{", "{")

        return output



class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 设置响应状态码
        self.send_response(200)

        # 设置响应头（指定内容类型为纯文本）
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        # 发送响应内容（需编码为字节流）
        self.wfile.write(DataGetter().homepage.encode('utf-8'))


def run_server():
    try:
        server_address = ('', int(config['server_port']))  # 侦听所有接口的8000端口
        httpd = HTTPServer(server_address, RequestHandler)
        print(f"Server started on port {config['server_port']}...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("KeyboardInterrupt accepted. Exiting")
        exit()


if __name__ == "__main__":
    run_server()
