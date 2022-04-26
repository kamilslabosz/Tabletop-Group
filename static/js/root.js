var vagabond = document.querySelectorAll(".root-faction-btn")[6]
var factions = document.querySelectorAll(".faction-div")

document.getElementById("riverfolk").addEventListener("click", function(){
    if (vagabond.innerHTML === "Vagabond"){
        vagabond.innerHTML = "Vagabond (both)";
    } else {
        vagabond.innerHTML = "Vagabond";
    }
    factions[4].classList.toggle('hidden');
    factions[5].classList.toggle('hidden');
    factions[6].classList.toggle('hidden');
});

document.getElementById("underworld").addEventListener("click", function(){
    factions[7].classList.toggle('hidden');
    factions[8].classList.toggle('hidden');
});

document.getElementById("marauder").addEventListener("click", function(){
    factions[9].classList.toggle('hidden');
    factions[10].classList.toggle('hidden');
});