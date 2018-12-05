% rebase('layout.tpl', title='Home Page', year=year)

<div class="jumbotron">
    <h1>War Cards</h1>
    <p class="lead">Either start a new game or continue a game with your personal code.</p>
</div>
<div>
    <h2>Start new game or continue a game</h2>
    <div class="row" >
        <div class="col-md-6">
            <form name="NewGame" action="/new" method="get">
                Name:<input type="text" name="txtName" value='' /><input class="btn btn-primary" type="submit" value="Start New">
            </form>



        </div>
        <div class="col-md-6">
            <form name="ContinueGame" action="/Continue" method="get">
                Code:<input type="text" name="txtCode" value='' /> <input class="btn btn-primary" type="submit" value="Continue">
            </form>
        </div>
    </div>
</div>
