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
        <h5>Your Score: {{userScore}}</h5>
        %for c in userCards:
            <img src="/static/deck/{{c[0]}}/{{c[1]}}.png">
        %end
    </div>
    <div class="col-md-6">
        <h3>Robo card</h3>
        <h5>Robo Score: {{roboScore}}</h5>
        %for c in roboCards:
            <img src="/static/deck/{{c[0]}}/{{c[1]}}.png">
        %end
    </div>
</div>
<div class="row">
    <div class="col-md-4">
        <a href="/game/{{userCards}}/{{roboCards}}/{{code}}">Play Next Hand</a>
    </div>
</div>

