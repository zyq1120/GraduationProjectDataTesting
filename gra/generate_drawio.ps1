$ErrorActionPreference = "Stop"

function X([string]$s) {
    if ($null -eq $s) { return "" }
    return [System.Security.SecurityElement]::Escape($s)
}

function New-Diagram {
    param(
        [string]$Path,
        [string]$Name,
        [string]$Caption,
        [array]$Nodes,
        [array]$Edges,
        [int]$W = 1800,
        [int]$H = 1100
    )

    $t = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
    $out = New-Object System.Collections.Generic.List[string]
    $out.Add('<mxfile host="app.diagrams.net" modified="' + $t + '" agent="Copilot" version="24.7.17" type="device">')
    $out.Add('  <diagram name="' + (X $Name) + '" id="' + [guid]::NewGuid().ToString() + '">')
    $out.Add('    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="' + $W + '" pageHeight="' + $H + '" math="0" shadow="0">')
    $out.Add('      <root>')
    $out.Add('        <mxCell id="0"/>')
    $out.Add('        <mxCell id="1" parent="0"/>')

    foreach ($n in $Nodes) {
        $style = if ($n.style) { $n.style } else { 'rounded=1;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=none;fontColor=#000000;' }
        $out.Add('        <mxCell id="' + $n.id + '" value="' + (X $n.text) + '" style="' + $style + '" vertex="1" parent="1">')
        $out.Add('          <mxGeometry x="' + $n.x + '" y="' + $n.y + '" width="' + $n.w + '" height="' + $n.h + '" as="geometry"/>')
        $out.Add('        </mxCell>')
    }

    foreach ($e in $Edges) {
        $style = if ($e.style) { $e.style } else { 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;endArrow=block;endFill=0;' }
        $out.Add('        <mxCell id="' + $e.id + '" value="' + (X $e.label) + '" style="' + $style + '" edge="1" parent="1" source="' + $e.from + '" target="' + $e.to + '">')
        $out.Add('          <mxGeometry relative="1" as="geometry"/>')
        $out.Add('        </mxCell>')
    }

    $out.Add('        <mxCell id="caption" value="' + (X $Caption) + '" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontColor=#000000;" vertex="1" parent="1">')
    $out.Add('          <mxGeometry x="300" y="' + ($H - 70) + '" width="1200" height="30" as="geometry"/>')
    $out.Add('        </mxCell>')

    $out.Add('      </root>')
    $out.Add('    </mxGraphModel>')
    $out.Add('  </diagram>')
    $out.Add('</mxfile>')

    Set-Content -Path $Path -Value ($out -join "`r`n") -Encoding UTF8
}

$dir = 'c:\working\GraduationProjectDataTesting\gra'

# F2-1
New-Diagram -Path "$dir\F2-1_BS_architecture.drawio" -Name "F2-1" -Caption "图 2-1 系统 B/S 架构与前后端分离示意图" -Nodes @(
@{id='n1';text='Browser Client';x=80;y=120;w=170;h=60},
@{id='n2';text='Vue Frontend';x=300;y=120;w=210;h=60},
@{id='n3';text='Spring Boot Backend';x=590;y=120;w=240;h=60},
@{id='n4';text='Python AI Service';x=910;y=120;w=210;h=60},
@{id='n5';text='MySQL';x=590;y=280;w=150;h=60},
@{id='n6';text='MinIO';x=790;y=280;w=150;h=60},
@{id='n7';text='Redis';x=990;y=280;w=150;h=60}
) -Edges @(
@{id='e1';from='n1';to='n2';label='HTTPS'},@{id='e2';from='n2';to='n3';label='REST JWT'},@{id='e3';from='n3';to='n4';label='AI call'},@{id='e4';from='n3';to='n5';label='data'},@{id='e5';from='n3';to='n6';label='files'},@{id='e6';from='n3';to='n7';label='cache'}
)

# F2-2
New-Diagram -Path "$dir\F2-2_OCR_flow.drawio" -Name "F2-2" -Caption "图 2-2 OCR 基本处理流程示意图" -Nodes @(
@{id='n1';text='Input image/PDF';x=120;y=180;w=170;h=60},
@{id='n2';text='Preprocess';x=340;y=180;w=170;h=60},
@{id='n3';text='OCR detect+recognize';x=560;y=180;w=190;h=60},
@{id='n4';text='Layout/table rebuild';x=800;y=180;w=180;h=60},
@{id='n5';text='Confidence check';x=1030;y=180;w=170;h=60},
@{id='n6';text='Structured OCR result';x=1250;y=180;w=200;h=60}
) -Edges @(
@{id='e1';from='n1';to='n2';label=''},@{id='e2';from='n2';to='n3';label=''},@{id='e3';from='n3';to='n4';label=''},@{id='e4';from='n4';to='n5';label=''},@{id='e5';from='n5';to='n6';label=''}
)

# F3-1
New-Diagram -Path "$dir\F3-1_roles_permissions.drawio" -Name "F3-1" -Caption "图 3-1 系统用户角色与权限关系图" -Nodes @(
@{id='n1';text='System User';x=80;y=220;w=130;h=60;style='ellipse;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=none;fontColor=#000000;'},
@{id='n2';text='SUPER_ADMIN';x=280;y=70;w=180;h=50},@{id='n3';text='ADMIN';x=280;y=140;w=180;h=50},@{id='n4';text='OPERATOR';x=280;y=210;w=180;h=50},@{id='n5';text='AUDITOR';x=280;y=280;w=180;h=50},@{id='n6';text='USER';x=280;y=350;w=180;h=50},
@{id='n7';text='User/Role Mgmt';x=560;y=70;w=200;h=50},@{id='n8';text='Template Mgmt';x=560;y=140;w=200;h=50},@{id='n9';text='Upload/Process';x=560;y=210;w=200;h=50},@{id='n10';text='Review Workbench';x=560;y=280;w=200;h=50},@{id='n11';text='Audit Approval';x=560;y=350;w=200;h=50},@{id='n12';text='Dashboard Export';x=560;y=420;w=200;h=50}
) -Edges @(
@{id='e1';from='n1';to='n2';label=''},@{id='e2';from='n1';to='n3';label=''},@{id='e3';from='n1';to='n4';label=''},@{id='e4';from='n1';to='n5';label=''},@{id='e5';from='n1';to='n6';label=''},
@{id='e6';from='n2';to='n7';label='all'},@{id='e7';from='n2';to='n8';label='all'},@{id='e8';from='n2';to='n9';label='all'},@{id='e9';from='n2';to='n10';label='all'},@{id='e10';from='n2';to='n11';label='all'},@{id='e11';from='n2';to='n12';label='all'},
@{id='e12';from='n4';to='n9';label='do'},@{id='e13';from='n4';to='n10';label='do'},@{id='e14';from='n5';to='n11';label='approve'},@{id='e15';from='n6';to='n9';label='upload'}
)

# F3-2
New-Diagram -Path "$dir\F3-2_doc_recognition_extraction.drawio" -Name "F3-2" -Caption "图 3-2 教务材料智能识别与信息抽取流程示意图" -Nodes @(
@{id='n1';text='Upload';x=90;y=180;w=120;h=55},@{id='n2';text='Store file metadata';x=260;y=170;w=170;h=75},@{id='n3';text='AI orchestrator';x=480;y=180;w=140;h=55},@{id='n4';text='OCR';x=680;y=120;w=110;h=55},@{id='n5';text='NLP extract';x=680;y=200;w=110;h=55},@{id='n6';text='Confidence OK?';x=870;y=170;w=130;h=70;style='rhombus;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=none;fontColor=#000000;'},@{id='n7';text='LLM fallback';x=1060;y=260;w=130;h=55},@{id='n8';text='Merge structured result';x=1060;y=100;w=190;h=55},@{id='n9';text='Pending review';x=1320;y=170;w=140;h=55}
) -Edges @(
@{id='e1';from='n1';to='n2';label=''},@{id='e2';from='n2';to='n3';label=''},@{id='e3';from='n3';to='n4';label=''},@{id='e4';from='n4';to='n5';label=''},@{id='e5';from='n5';to='n6';label=''},@{id='e6';from='n6';to='n8';label='yes'},@{id='e7';from='n6';to='n7';label='no'},@{id='e8';from='n7';to='n8';label=''},@{id='e9';from='n8';to='n9';label=''}
)

# F3-3
New-Diagram -Path "$dir\F3-3_human_in_loop_audit.drawio" -Name "F3-3" -Caption "图 3-3 人机协同校对与审核流程示意图" -Nodes @(
@{id='n1';text='Pending task';x=120;y=180;w=130;h=55},@{id='n2';text='Review workbench';x=300;y=170;w=170;h=75},@{id='n3';text='Field edit';x=520;y=120;w=120;h=55},@{id='n4';text='Save draft';x=520;y=220;w=120;h=55},@{id='n5';text='Submit audit';x=690;y=170;w=130;h=55},@{id='n6';text='Approved?';x=870;y=160;w=130;h=70;style='rhombus;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=none;fontColor=#000000;'},@{id='n7';text='Archive';x=1060;y=100;w=120;h=55},@{id='n8';text='Reject back';x=1060;y=240;w=120;h=55}
) -Edges @(
@{id='e1';from='n1';to='n2';label=''},@{id='e2';from='n2';to='n3';label=''},@{id='e3';from='n2';to='n4';label=''},@{id='e4';from='n4';to='n2';label='loop'},@{id='e5';from='n3';to='n5';label=''},@{id='e6';from='n5';to='n6';label=''},@{id='e7';from='n6';to='n7';label='yes'},@{id='e8';from='n6';to='n8';label='no'},@{id='e9';from='n8';to='n2';label='fix'}
)

# T3-2 table
$cell = 'shape=rectangle;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=none;fontColor=#000000;'
New-Diagram -Path "$dir\T3-2_statistics_result_requirements.drawio" -Name "T3-2" -Caption "表 3-2 数据统计与结果管理功能需求说明表" -W 1600 -H 900 -Nodes @(
@{id='h1';text='Module';x=80;y=120;w=200;h=50;style=$cell},@{id='h2';text='Feature';x=280;y=120;w=420;h=50;style=$cell},@{id='h3';text='Input';x=700;y=120;w=250;h=50;style=$cell},@{id='h4';text='Output';x=950;y=120;w=250;h=50;style=$cell},@{id='h5';text='Priority';x=1200;y=120;w=140;h=50;style=$cell},
@{id='r1c1';text='Statistics';x=80;y=170;w=200;h=70;style=$cell},@{id='r1c2';text='overview trend distribution';x=280;y=170;w=420;h=70;style=$cell},@{id='r1c3';text='status date range';x=700;y=170;w=250;h=70;style=$cell},@{id='r1c4';text='dashboard charts';x=950;y=170;w=250;h=70;style=$cell},@{id='r1c5';text='High';x=1200;y=170;w=140;h=70;style=$cell},
@{id='r2c1';text='Result mgmt';x=80;y=240;w=200;h=70;style=$cell},@{id='r2c2';text='search detail trace';x=280;y=240;w=420;h=70;style=$cell},@{id='r2c3';text='doc type keyword';x=700;y=240;w=250;h=70;style=$cell},@{id='r2c4';text='structured view';x=950;y=240;w=250;h=70;style=$cell},@{id='r2c5';text='High';x=1200;y=240;w=140;h=70;style=$cell},
@{id='r3c1';text='Export';x=80;y=310;w=200;h=70;style=$cell},@{id='r3c2';text='files audits reports';x=280;y=310;w=420;h=70;style=$cell},@{id='r3c3';text='filters format';x=700;y=310;w=250;h=70;style=$cell},@{id='r3c4';text='excel reports';x=950;y=310;w=250;h=70;style=$cell},@{id='r3c5';text='Medium';x=1200;y=310;w=140;h=70;style=$cell}
) -Edges @()

# F4-2
New-Diagram -Path "$dir\F4-2_function_modules.drawio" -Name "F4-2" -Caption "图 4-2 系统功能模块划分图" -Nodes @(
@{id='n1';text='System';x=730;y=60;w=180;h=55},@{id='n2';text='Frontend';x=170;y=220;w=150;h=55},@{id='n3';text='Backend';x=480;y=220;w=150;h=55},@{id='n4';text='AI layer';x=790;y=220;w=150;h=55},@{id='n5';text='Infra';x=1100;y=220;w=150;h=55},
@{id='n6';text='Files';x=120;y=340;w=100;h=50},@{id='n7';text='Classify';x=240;y=340;w=100;h=50},@{id='n8';text='Workbench';x=120;y=410;w=100;h=50},@{id='n9';text='Dashboard';x=240;y=410;w=100;h=50},
@{id='n10';text='Auth';x=430;y=340;w=100;h=50},@{id='n11';text='Audit';x=550;y=340;w=100;h=50},@{id='n12';text='Template';x=430;y=410;w=100;h=50},@{id='n13';text='Export';x=550;y=410;w=100;h=50},
@{id='n14';text='OCR';x=740;y=340;w=100;h=50},@{id='n15';text='NLP';x=860;y=340;w=100;h=50},@{id='n16';text='LLM';x=740;y=410;w=100;h=50},@{id='n17';text='Orchestrator';x=860;y=410;w=100;h=50},
@{id='n18';text='MySQL';x=1050;y=340;w=100;h=50},@{id='n19';text='MinIO';x=1170;y=340;w=100;h=50},@{id='n20';text='Redis';x=1050;y=410;w=100;h=50},@{id='n21';text='Logs';x=1170;y=410;w=100;h=50}
) -Edges @(
@{id='e1';from='n1';to='n2';label=''},@{id='e2';from='n1';to='n3';label=''},@{id='e3';from='n1';to='n4';label=''},@{id='e4';from='n1';to='n5';label=''},@{id='e5';from='n2';to='n6';label=''},@{id='e6';from='n2';to='n7';label=''},@{id='e7';from='n2';to='n8';label=''},@{id='e8';from='n2';to='n9';label=''},@{id='e9';from='n3';to='n10';label=''},@{id='e10';from='n3';to='n11';label=''},@{id='e11';from='n3';to='n12';label=''},@{id='e12';from='n3';to='n13';label=''},@{id='e13';from='n4';to='n14';label=''},@{id='e14';from='n4';to='n15';label=''},@{id='e15';from='n4';to='n16';label=''},@{id='e16';from='n4';to='n17';label=''},@{id='e17';from='n5';to='n18';label=''},@{id='e18';from='n5';to='n19';label=''},@{id='e19';from='n5';to='n20';label=''},@{id='e20';from='n5';to='n21';label=''}
)

# F4-3
New-Diagram -Path "$dir\F4-3_upload_processing_flow.drawio" -Name "F4-3" -Caption "图 4-3 文档上传与处理流程图" -Nodes @(
@{id='n1';text='Upload';x=80;y=180;w=120;h=55},@{id='n2';text='Validate';x=240;y=180;w=120;h=55},@{id='n3';text='Store MinIO';x=400;y=180;w=130;h=55},@{id='n4';text='Insert document_file';x=580;y=180;w=170;h=55},@{id='n5';text='Queue';x=800;y=180;w=110;h=55},@{id='n6';text='Call AI';x=960;y=180;w=110;h=55},@{id='n7';text='Write extract result';x=1120;y=180;w=170;h=55},@{id='n8';text='Update status';x=1340;y=180;w=140;h=55}
) -Edges @(
@{id='e1';from='n1';to='n2';label=''},@{id='e2';from='n2';to='n3';label='ok'},@{id='e3';from='n3';to='n4';label=''},@{id='e4';from='n4';to='n5';label=''},@{id='e5';from='n5';to='n6';label=''},@{id='e6';from='n6';to='n7';label=''},@{id='e7';from='n7';to='n8';label=''}
)

# F4-4
New-Diagram -Path "$dir\F4-4_intelligent_and_manual_flow.drawio" -Name "F4-4" -Caption "图 4-4 智能处理与人工校对流程图" -Nodes @(
@{id='n1';text='Start';x=100;y=170;w=120;h=55},@{id='n2';text='OCR + NLP';x=260;y=170;w=130;h=55},@{id='n3';text='Confidence OK?';x=450;y=160;w=130;h=70;style='rhombus;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=none;fontColor=#000000;'},@{id='n4';text='LLM fallback';x=640;y=240;w=130;h=55},@{id='n5';text='Structured output';x=640;y=100;w=130;h=55},@{id='n6';text='Manual review';x=830;y=170;w=130;h=55},@{id='n7';text='Audit';x=1010;y=170;w=110;h=55},@{id='n8';text='Archive';x=1170;y=100;w=110;h=55},@{id='n9';text='Reject';x=1170;y=240;w=110;h=55}
) -Edges @(
@{id='e1';from='n1';to='n2';label=''},@{id='e2';from='n2';to='n3';label=''},@{id='e3';from='n3';to='n5';label='yes'},@{id='e4';from='n3';to='n4';label='no'},@{id='e5';from='n4';to='n5';label=''},@{id='e6';from='n5';to='n6';label=''},@{id='e7';from='n6';to='n7';label=''},@{id='e8';from='n7';to='n8';label='yes'},@{id='e9';from='n7';to='n9';label='no'},@{id='e10';from='n9';to='n6';label='fix'}
)

# F5-1
$entity = 'shape=rectangle;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=none;fontColor=#000000;align=left;spacingLeft=6;'
New-Diagram -Path "$dir\F5-1_database_er.drawio" -Name "F5-1" -Caption "图 5-1 系统数据库 E-R 关系图" -W 1900 -H 1200 -Nodes @(
@{id='n1';text='sys_user|PK id|username';x=80;y=80;w=190;h=110;style=$entity},@{id='n2';text='sys_role|PK id|role_key';x=80;y=280;w=190;h=110;style=$entity},@{id='n3';text='sys_user_role|PK id|FK user_id|FK role_id';x=320;y=180;w=220;h=130;style=$entity},@{id='n4';text='document_file|PK id|FK user_id|FK template_id';x=620;y=70;w=250;h=140;style=$entity},@{id='n5';text='sys_doc_template|PK id|template_code';x=940;y=70;w=220;h=110;style=$entity},@{id='n6';text='document_extract_main|PK id|FK file_id|FK template_id';x=620;y=270;w=260;h=140;style=$entity},@{id='n7';text='document_extract_detail|PK id|FK file_id|FK main_id';x=940;y=270;w=250;h=140;style=$entity},@{id='n8';text='audit_record|PK id|FK file_id|FK auditor_id';x=1240;y=120;w=240;h=120;style=$entity},@{id='n9';text='sys_task_log|PK id|FK file_id';x=1240;y=290;w=240;h=110;style=$entity},@{id='n10';text='document_ocr_raw|PK id|FK file_id';x=620;y=460;w=240;h=110;style=$entity}
) -Edges @(
@{id='e1';from='n1';to='n3';label='1:N'},@{id='e2';from='n2';to='n3';label='1:N'},@{id='e3';from='n1';to='n4';label='1:N'},@{id='e4';from='n5';to='n4';label='1:N'},@{id='e5';from='n4';to='n6';label='1:1'},@{id='e6';from='n5';to='n6';label='1:N'},@{id='e7';from='n6';to='n7';label='1:N'},@{id='e8';from='n4';to='n7';label='1:N'},@{id='e9';from='n4';to='n8';label='1:N'},@{id='e10';from='n1';to='n8';label='1:N'},@{id='e11';from='n4';to='n9';label='1:N'},@{id='e12';from='n4';to='n10';label='1:N'}
)

Write-Output "DONE"
