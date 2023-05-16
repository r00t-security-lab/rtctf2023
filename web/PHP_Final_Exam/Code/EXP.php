<?php
class model{
    public $stdAns;
    public $ans;
}
$tmp = new model();
$tmp->stdAns="123";
$tmp->ans="123";
echo urlencode(serialize($tmp));