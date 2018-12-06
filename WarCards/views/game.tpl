% rebase('layout.tpl', title='Home Page', year=year)
<div class="row">
    <div class="col-md-12">
        <h2>User:{{user}}</h2>
        <h3>Game Code:{{code}}</h3>
    </div>
</div>
<div class="row">
    <div class="col-md-6">
        <h3>Your card</h3>
        <img src="/static/deck/{{userCard[0]}}/{{userCard[1]}}.png">
    </div>
    <div class="col-md-6">
        <h3>Robo card</h3>
        <img src="/static/deck/{{roboCard[0]}}/{{roboCard[1]}}.png">
    </div>
</div>
<div class="row">
    <div class="col-md-4">
        <a href="/game/{{userCard}}/{{roboCard}}/{{code}}">Play Next Hand</a>
    </div>
</div>

