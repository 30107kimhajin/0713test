<!DOCTYPE html>
<html lang="ko">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>열섬현상과 전력수요의 관계</title>

<script src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body{
    margin:0;
    padding:30px;
    font-family:Arial, Helvetica, sans-serif;
    background:#f4f6f8;
}

h1{
    color:#0b5ed7;
}

.card{
    background:white;
    padding:20px;
    border-radius:10px;
    margin-bottom:20px;
    box-shadow:0 2px 8px rgba(0,0,0,0.1);
}

canvas{
    margin-top:20px;
}

select,input{
    padding:8px;
    margin:5px;
}

.result{
    background:#eef8ff;
    border-left:5px solid #2196F3;
    padding:15px;
    margin-top:20px;
}

</style>

</head>

<body>

<h1>열섬현상과 전력수요의 관계</h1>

<h3>탐구 질문</h3>

<p><b>열섬 강도가 커질수록 전력수요도 증가할까?</b></p>

<div class="card">

<h2>데이터 확인</h2>

<p>

사용 데이터 : 2025년 시간별 자료

<br>

서울 기온

<br>

양평 기온

<br>

전력수요

</p>

<label>날짜 선택</label>

<input type="date" id="dateFilter">

</div>

<div class="card">

<h2>열섬현상 분석</h2>

<canvas id="tempChart"></canvas>

<canvas id="heatChart"></canvas>

</div>

<div class="card">

<h2>전력수요 분석</h2>

<canvas id="powerChart"></canvas>

</div>

<div class="card">

<h2>상관관계 분석</h2>

<canvas id="scatterChart"></canvas>

<div id="corrText" class="result"></div>

</div>

<div class="card">

<h2>탐구 결과</h2>

<div id="summary"></div>

</div>

<script>

let seoul=[]
let yang=[]
let power=[]
// -------------------------
// CSV 읽기 함수
// -------------------------

function loadCSV(file){

    return new Promise(resolve=>{

        Papa.parse(file,{

            download:true,

            header:true,

            complete:function(result){

                resolve(result.data);

            }

        });

    });

}

// -------------------------
// 데이터 불러오기
// -------------------------

Promise.all([

    loadCSV("서울_기온.csv"),

    loadCSV("양평_기온.csv"),

    loadCSV("전력수요.csv")

]).then(function(data){

    seoul=data[0];
    yang=data[1];
    power=data[2];

    mergeData();

});


// -------------------------
// 데이터 병합
// -------------------------

let merged=[];

function mergeData(){

    merged=[];

    let powerMap={};

    power.forEach(function(d){

        powerMap[d["일시"]]=Number(d["전력수요(MWh)"]);

    });

    let yangMap={};

    yang.forEach(function(d){

        yangMap[d["일시"]]=Number(d["기온(°C)"]);

    });

    seoul.forEach(function(d){

        let date=d["일시"];

        if(yangMap[date]!=null && powerMap[date]!=null){

            merged.push({

                date:date,

                seoul:Number(d["기온(°C)"]),

                yang:Number(yangMap[date]),

                heat:Number(d["기온(°C)"])-Number(yangMap[date]),

                power:Number(powerMap[date])

            });

        }

    });

    drawTempChart();

    drawHeatChart();

    drawPowerChart();

    drawScatter();

}
// -------------------------
// ① 서울·양평 기온 변화
// -------------------------

function drawTempChart(){

const ctx=document.getElementById("tempChart");

new Chart(ctx,{

type:"line",

data:{

labels:merged.map(d=>d.date),

datasets:[

{

label:"서울",

data:merged.map(d=>d.seoul),

borderColor:"red",

fill:false

},

{

label:"양평",

data:merged.map(d=>d.yang),

borderColor:"blue",

fill:false

}

]

},

options:{

responsive:true,

plugins:{

title:{

display:true,

text:"서울과 양평 기온 변화"

}

},

scales:{

x:{

display:false

}

}

}

});

}

// -------------------------
// ② 열섬강도 변화
// -------------------------

function drawHeatChart(){

const ctx=document.getElementById("heatChart");

new Chart(ctx,{

type:"line",

data:{

labels:merged.map(d=>d.date),

datasets:[

{

label:"열섬 강도",

data:merged.map(d=>d.heat),

borderColor:"orange",

fill:false

}

]

},

options:{

responsive:true,

plugins:{

title:{

display:true,

text:"열섬 강도(서울-양평)"

}

},

scales:{

x:{

display:false

}

}

}

});

}

// -------------------------
// ③ 전력수요 변화
// -------------------------

function drawPowerChart(){

const ctx=document.getElementById("powerChart");

new Chart(ctx,{

type:"line",

data:{

labels:merged.map(d=>d.date),

datasets:[

{

label:"전력수요(MWh)",

data:merged.map(d=>d.power),

borderColor:"green",

fill:false

}

]

},

options:{

responsive:true,

plugins:{

title:{

display:true,

text:"전력수요 변화"

}

},

scales:{

x:{

display:false

}

}

}

});

}
// -------------------------
// 산점도 + 추세선
// -------------------------

function drawScatter(){

    let points = merged.map(d=>({
        x:d.heat,
        y:d.power
    }));

    // 평균
    let meanX = merged.reduce((a,b)=>a+b.heat,0)/merged.length;
    let meanY = merged.reduce((a,b)=>a+b.power,0)/merged.length;

    // 기울기 계산
    let num = 0;
    let den = 0;

    for(let i=0;i<merged.length;i++){

        num += (merged[i].heat-meanX)*(merged[i].power-meanY);
        den += (merged[i].heat-meanX)*(merged[i].heat-meanX);

    }

    let slope = num/den;
    let intercept = meanY - slope*meanX;

    let minX = Math.min(...merged.map(d=>d.heat));
    let maxX = Math.max(...merged.map(d=>d.heat));

    let trend = [

        {
            x:minX,
            y:slope*minX+intercept
        },

        {
            x:maxX,
            y:slope*maxX+intercept
        }

    ];

    const ctx=document.getElementById("scatterChart");

    new Chart(ctx,{

        type:"scatter",

        data:{

            datasets:[

                {
                    label:"데이터",
                    data:points
                },

                {
                    label:"추세선",
                    data:trend,
                    type:"line",
                    fill:false
                }

            ]

        }

    });

    calcCorrelation();

}

// -------------------------
// 피어슨 상관계수
// -------------------------

function calcCorrelation(){

    let x = merged.map(d=>d.heat);
    let y = merged.map(d=>d.power);

    let meanX = x.reduce((a,b)=>a+b)/x.length;
    let meanY = y.reduce((a,b)=>a+b)/y.length;

    let num = 0;
    let denX = 0;
    let denY = 0;

    for(let i=0;i<x.length;i++){

        num += (x[i]-meanX)*(y[i]-meanY);

        denX += (x[i]-meanX)*(x[i]-meanX);

        denY += (y[i]-meanY)*(y[i]-meanY);

    }

    let r = num/Math.sqrt(denX*denY);

    let text="";

    if(r>0.7){

        text="강한 양의 상관관계";

    }

    else if(r>0.3){

        text="약한 양의 상관관계";

    }

    else if(r<-0.7){

        text="강한 음의 상관관계";

    }

    else if(r<-0.3){

        text="약한 음의 상관관계";

    }

    else{

        text="상관관계가 약함";

    }

    document.getElementById("corrText").innerHTML=

    "<h3>피어슨 상관계수(r)</h3>"+

    "<h2>"+r.toFixed(3)+"</h2>"+

    "<b>"+text+"</b><br><br>"+

    "※ 상관관계는 인과관계를 의미하지 않습니다.";

    document.getElementById("summary").innerHTML=

    "계산된 피어슨 상관계수는 <b>"+

    r.toFixed(3)+

    "</b>이며 <b>"+

    text+

    "</b>로 해석됩니다.<br><br>"+

    "열섬 강도와 전력수요의 관계는 실제 데이터 분석 결과를 기반으로 나타낸 것이며, 상관관계만으로 원인과 결과를 단정할 수 없습니다.";

}

</script>

</body>

</html>
