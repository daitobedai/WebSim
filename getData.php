<?php
    $code = $_GET['exp'];
    $type = $_GET['type'];
    $stock = $_GET['stock'];
    //$code = 'avg(close, 5) < max(close, 3)'; $type = 1; $stock = '00001.sz';
    $stockArray = explode('.', $stock);
    //alert($type);
    $output = shell_exec('python src/exparsingFinal.py '.$type.' "'.$code.'" '.$stockArray[0].' '.$stockArray[1]);
    echo $output;
?>
