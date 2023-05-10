<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="./basic.css" rel="stylesheet" type="text/css">
    <title>PHP Final Exam</title>
    <!-- 备份源码是个好习惯~ -->
</head>
<body>
<?php
// CTFer就该这么写试卷！（当然不是因为懒得写前端啦）
error_reporting(0);
// PHP=7.0.9
include("flag1.php");
include("flag2.php");
class prob_one{
    private $assignment;
    public $ans;
    public $title;
    public function __construct(){
        $this->ans="找到试卷就算成功!";
        $this->assignment="ea5y";
        $this->title="ans1";
    }
    public function test($rep){
        if($rep===$this->assignment){
            return 1;
        }
        return 0;
    }
}

class prob_two{
    private $assignment;
    public $ans;
    public $title;
    public function __construct(){
        $this->ans="Easy!";
        $this->assignment="1357abcdefgh";
        $this->title="ans2";
    }
    public function test($rep){
        if(is_numeric($rep) and $rep==$this->assignment){
            return 1;
        }
        return 0;
    }
}

class prob_three{
    public $ans;
    public $title;
    public $_title;
    public function __construct(){
        $this->ans="Cool!";
        $this->title="ans3";
        $this->_title="_ans3";
    }
    public function test($rep1, $rep2){
        if($rep1 !== $rep2){
            if(md5($rep1) == md5($rep2)){
                return 1;
            }
        }
        return 0;
    }
}

class model{
    public $stdAns;
    public $ans;
    public function __construct(){
        $this->$stdAns="CTF";
    }

    public function __wakeup(){
        $this->stdAns="r00tCTF";
        $this->ans="rootCTF";
    }

    public function __destruct(){
        global $prob4;
        if($this->stdAns == $this->ans){
            $prob4->check = 1;
            return 1;
        }
        $prob4->check = 0;
        return 0;
    }
}

class prob_four{
    private $assignment;
    public $ans;
    public $title;
    public $check;
    public function __construct(){
        $this->ans="Well Done!";
        $this->title="ans4";
    }
    public function test(){
        if($this->check==1){
            return 1;
        }
        return 0;
    }
}


class prob_five{
    private $assignment;
    public $ans;
    public $title;
    public $file;
    public $secret;
    public function __construct(){
        $this->ans="Wow~";
        $this->title="ans5";
        $this->file="file";
        include("secret.php");
        $this->secret=$secret;
    }
    public function test($rep){
        if($this->secret==$rep){
            return 1;
        }
        return 0;
    }
}

// class prob_five{

// }

    $score = 0;
    $check = 0;
    $msg = array(
        "未作答", "未作答", "未作答", "未作答", "未作答"
    );
    $tt = array(
        "找到题目在哪！", "??", "??", "??", "??"
    );
    $p5 = "nothing";
    $fn = "考试开始了，速速作答！";
    $prob1 = new prob_one();
    if(isset($_GET[$prob1->title])){
        $check = 1;
        $prm = $_GET[$prob1->title];
        if($prob1->test($prm)==1){
            $score+=20;
            $msg[0] = $prob1->ans;
        } else {
            $msg[0] = "WA咯~";
        }
    } 

    $prob2 = new prob_two();
    if(isset($_GET[$prob2->title])){
        $check = 1;
        $prm = (int)$_GET[$prob2->title];
        if($prob2->test($prm)==1){
            $score+=20;
            $msg[1] = $prob2->ans;
            $tt[1] = "简单的让字符串和数字相等";
        } else {
            $msg[1] = "WA咯~";
        }
    } 
    
    $prob3 = new prob_three();
    if(isset($_GET[$prob3->title]) && isset($_GET[$prob3->_title])){
        $check = 1;
        $prm = $_GET[$prob3->title];
        $_prm = $_GET[$prob3->_title];

        if($prob3->test($prm, $_prm)==1){
            $score+=20;
            $msg[2] = $prob3->ans;
            $tt[2] = "区区MD5碰撞";
        } else {
            $msg[2] = "WA咯~";
        }
    }

    $prob4 = new prob_four();
    if(isset($_GET[$prob4->title])){
        $check = 1;
        try{
            $tmp = unserialize($_GET[$prob4->title]);
            if($prob4->model==FALSE && $prob4->check!=1){
                throw New Exception("Err with unserialize!");
            }
            if($prob4->test()==1){
                $score+=20;
                $msg[3] = $prob4->ans;
                $tt[3] = "EZ的PHP反序列化";
            } else {
                $msg[3] = "WA咯~";
            }
        } catch (Exception $e){
            $msg[3] = "WA咯~";
        }
    }

    $prob5 = new prob_five();
    if(isset($_GET[$prob5->file])){
        $check = 1;
        $prm = $_GET[$prob5->file];
        if(!preg_match("/flag|file|data|\\.\\.\\/|^\\/.*/i", $prm)){
            $file = file_get_contents($prm);
        } else {
            $file = "No cheat!";
        }
    }
    if(isset($_GET[$prob5->title])){
        $check = 1;
        $prm = $_GET[$prob5->title];
        if($prob5->test($prm)==1){
            $score+=20;
            $msg[4] = $prob5->ans;
            $tt[4] = "PHP的伪协议";
        } else {
            $msg[4] = "WA咯~";
        }
    }
    

    if($check==1){
        if($score<60){
            $fn = "什么，居然不及格！不许摆烂！";
        } else if($score<80){
            $fn = "及格就算成功！".$flag1;
        } else if($score<100){
            $fn = "离满分还差一点！".$flag1;
        } else {
            $fn = "满分耶~".$flag2;
        }
    }

?>
<div class="Title">
    <h1>PHP期末考试</h1>
    <span class="info">姓名: </span><span class="cot">Festu</span>
    <span class="info">分数: </span><span class="cot"><?=$score;?></span>
    <span class="info">作答情况: </span><span class="cot"><?=$fn;?></span>
</div>
<h2 class="pbTitle">试题列表: </h2>
<div class="problem">
    <span class="info">题目1:</span>
    <span class="cot"><?=$tt[0]?></span>
    <span class="info">答题状况:</span> 
    <span class="cot"><?=$msg[0]?></span>
</div>
<div class="problem">
    <span class="info">题目2:</span>
    <span class="cot"><?=$tt[1]?></span>
    <span class="info">答题状况:</span> 
    <span class="cot"><?=$msg[1]?></span>
</div>
<div class="problem">
    <span class="info">题目3:</span>
    <span class="cot"><?=$tt[2]?></span>
    <span class="info">答题状况:</span> 
    <span class="cot"><?=$msg[2]?></span>
</div>
<div class="problem">
    <span class="info">题目4:</span>
    <span class="cot"><?=$tt[3]?></span>
    <span class="info">答题状况:</span> 
    <span class="cot"><?=$msg[3]?></span>
</div>
<div class="problem">
    <span class="info">题目5:</span>
    <span class="cot"><?=$tt[4]?></span>
    <span class="info">答题状况:</span> 
    <span class="cot"><?=$msg[4]?></span>
    <span class="info">File信息:</span> 
    <span class="cot"><?=$file?></span>
</div>
</body>
</html>

