<?php
class TopFile {

    public $fs;

    public function readFile() {
        $fs = fopen("data/top10.csv", a);
    }
}
?>
