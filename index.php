<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">

    <title>Theme Template for Bootstrap</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap theme -->
    <link href="css/bootstrap-theme.min.css" rel="stylesheet">

    <!-- Custom styles for this template-->
    <link href="css/theme.css" rel="stylesheet">
     
  </head>

  <body role="document">

    <nav class="navbar navbar-inverse navbar-static-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="./index">WebSim ZJU</a>
        </div>

        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="#">Home</a></li>
            <li><a href="#">Top 10</a></li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
            <li><a href="#">浙江大学17期SRTP 王禹杰小组</a></li>
            <!--<li><a href="./projectList">MY ALGORITHMS</a></li>
            <li><a href="./strategyList">STRATEGIES</a></li>
            <li><a href="./product">PRODUCTS</a></li>
            <li><a href="./projectList">HELP</a></li>
            <li><a href="./login">LOGIN</a></li>-->
          </ul>
        </div>
      </div>
    </nav>

    <div class="container">
      <div class="page-header">
        <h1 class="text-center">The Web Sim <small>made by 709 ZJU</small></h1>
        <p class="text-center">Make your own algorithms below</p>
      </div>

      <div class="row">
        <div class="input-group input-group-lg">
          <input type="text" class="form-control" id="code" placeholder="Your algorithm...">
          <span class="input-group-btn">
            <button class="btn btn-default" type="button" onclick="backTest()">Go!</button>
          </span>
        </div><!-- /input-group -->
      </div>
      <br/>

      <div class="row">
        <form class="form-inline">
          <div class="form-group col-md-offset-4">
            <div class="btn-group" data-toggle="buttons">
              <label class="btn btn-default active">
                <input type="radio" name="lanType" id="lanType1" value="expression" autocomplete="off" checked><strong> Expression</strong>
              </label>
              <label class="btn btn-info">
                <input type="radio" name="lanType" id="lanType2" value="python" autocomplete="off"><strong> Python Code</strong>
              </label>
            </div>
          </div>
          <div class="form-group col-md-offset-2">
            <label for="stockId">Select Stock </label>
            <select class="form-control" id="stockId">
              <option>000001.sz</option>
              <option>000002.sz</option>
              <option>000004.sz</option>
              <option>000005.sz</option>
              <option>000006.sz</option>
              <option>000007.sz</option>
              <option>000008.sz</option>
              <option>000009.sz</option>
              <option>000010.sz</option>
              <option>000012.sz</option>
              <option>000014.sz</option>
              <option>000016.sz</option>
              <option>000017.sz</option>
              <option>000018.sz</option>
              <option>000019.sz</option>
              <option>000020.sz</option>
              <option>000021.sz</option>
              <option>000022.sz</option>
              <option>000023.sz</option>
              <option>000024.sz</option>
              <option>000025.sz</option>
              <option>000026.sz</option>
              <option>000027.sz</option>
              <option>000028.sz</option>
              <option>000029.sz</option>
              <option>000031.sz</option>
              <option>000032.sz</option>
              <option>000033.sz</option>
              <option>000034.sz</option>
              <option>000035.sz</option>
              <option>000036.sz</option>
              <?php require 'stockSelect.php'; ?>
            </select>
          </div>
        </form>
      </div>

      <br/>
      <div id="content">
      
      </div>

    </div>
    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="Highstock-2.1.5/js/highstock.js"></script>
    <script src="Highstock-2.1.5/js/modules/exporting.js"></script>
    <script type="text/javascript">
    function backTest() {
        htmlobj=$.ajax({url:"panel.php",async:false});
        $("#content").html(htmlobj.responseText);

        var title = "";
        var code = document.getElementById("code").value;
        var type = document.getElementsByName("lanType")[0].checked == true ? 1: 0;
        var stock = document.getElementById("stockId").value;

        if (type)
            title += "Expression: ";
        else
            title += "Python: ";

        title += code;
        $("#panelTitle").html(title);
        
        $(function () {
            $.getJSON('getData.php', {exp: code, type: type, stock: stock}, function (data) {
                var isValid = data.isValid;
                var error = data.error;
                if (isValid == false) {
                    alert("avc");
                    warningobj = $.ajax({url:"warning.php",async:false});
                    $("#result").html(warningobj.responseText);
                    $("#warning").html(error);
                }
                else {
                // Create the chart
                $('#result').highcharts('StockChart', {
                    rangeSelector: {
                        selected: 1
                    },

                    title: {
                        text: 'Back Test Result of ' + stock
                    },

                    scrollbar: {
                        barBackgroundColor: 'gray',
                        barBorderRadius: 7,
                        barBorderWidth: 0,
                        buttonBackgroundColor: 'gray',
                        buttonBorderWidth: 0,
                        buttonBorderRadius: 7,
                        trackBackgroundColor: 'none',
                        trackBorderWidth: 1,
                        trackBorderRadius: 8,
                        trackBorderColor: '#CCC'
                    },

    
                    yAxis: [{
                        labels: {
                            align: 'right',
                            x: -3
                        },
                        title: {
                            text: 'Return'
                        },
                        height: '65%',
                        lineWidth: 2
                    }, {
                        labels: {
                            align: 'right',
                            x: -3
                        },
                        title: {
                            text: 'Bench'
                        },
                        top: '70%',
                        height: '30%',
                        offset: 0,
                        lineWidth: 2
                    }],

                    series: [{
                        name: 'Return',
                        data: data.data1,
                        fillColor : {
                            linearGradient : {
                                x1: 0,
                                y1: 1,
                                x2: 0,
                                y2: 0
                            },
                        stops : [
                                [0, Highcharts.getOptions().colors[0]],
                                [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                            ]
                        },
                        tooltip: {
                            valueDecimals: 2
                        }
                    },{
                        name: 'Bench Mark',
                        data: data.data2,
                        yAxis: 1,
                    }]
                });}
            });
        });
    }
	</script>

  </body>
</html>


