var buttons = ['root', 'ttrpg', 'bg-game', 'todo', 'contact', 'about'];
var gamePattern = [];
var userPattern = [];
var level = 0;
var gameOver = false;

$('.game').hide();
$('.game-over').hide();


$('#show-game').click(function() {
    $('#home-area').slideUp(500);
    setTimeout(function (){
      $('.game').slideDown();
      $('#start-game').click(function() {
        console.log('clicked');
        $('.game-over').hide();
        gamePattern = [];
        level = 0;
        gameOver = false;
        $('#start-game').html('Restart');
        setTimeout(function (){
          nextSequence();
        }, 1000);
    });
    }, 1000);
});


function nextSequence() {
  var randomNumber = (Math.floor(Math.random() * 6));
  var randomSquare = buttons[randomNumber];
  userPattern = [];
  level++;
  $('.level-counter').html("Level " + level);
  console.log(randomSquare);
  gamePattern.push(randomSquare);
  animatePress(randomSquare);
};


$('.game-btn').click(function () {
  var userChosenSquare = $(this).attr('id');
  userPattern.push(userChosenSquare);
  checkAnswer((userPattern.length-1));
  animatePress(userChosenSquare);
});

function animatePress(button){
  $("#" + button).fadeOut(300);
  $("#" + button).fadeIn();
};

function checkAnswer(answerIndex){
  if (userPattern[answerIndex] === gamePattern[answerIndex]){
  } else{
    gameOver = true;
    $('.container').toggleClass('wrong');
    setTimeout(function (){
        $('.container').toggleClass('wrong');
        $('.game-over').show();
    }, 200);

  };

  if ((userPattern.length === gamePattern.length) && (!gameOver)){
    setTimeout(function (){
      nextSequence();
    }, 1000);
  };
};