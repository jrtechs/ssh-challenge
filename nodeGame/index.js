//////////express server/library initalization
const port = 7777;

const express = require('express');

const app = express();

/**session data for login and storing preferences*/
const session = require('express-session');

/**Initializes sessions for login */
app.use(session(
    { secret: "private stuff for session seed or something",
            cookie: { maxAge: 6000000 }}
    ));


// makes working with post data easier
const bodyParser = require('body-parser');
app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies


//used for file io
const fs = require('fs');


/////////// express server/library initalization //////////////


// quick and dirty routes for server //

//add point to user
app.post("/stonks", (request, result)=>
    {
	    if(!request.session.hasOwnProperty("score"))
	    {
		    request.session.score = 0;
	    }
	    request.session.score = request.session.score + 1;
        result.end();
    });


//set the score to zero
app.post("/notStonks", (request, result)=>
    {
	    request.session.score = 0;
        result.send("Stonks :(");
    });


//check if user has over 100 points, display wining screen
//else: tell them to play again
app.get('/endGame', (req, res) =>
    {

	    if(!req.session.hasOwnProperty("score"))
	    {
		    req.session.score = 0;
	    }
	
	    console.log(req.session.score);
	    if(req.session.score > 100)
	    {
		    //fun zone
		    console.log("Someone won the game");
            res.write(fs.readFileSync("hint.html"));
	    }
	    else
	    {
		    res.write(fs.readFileSync("needHigherScore.html"));  
        }
        res.end();
    });


// sneaky login route
app.post('/login', (req, res) =>
    {
        if(req.body.password == "ritlugFunziesPassword")
        {
            req.session.loggedIn = true;
        }
        res.redirect('/');
    });


//prompt for login if not logged in
//else: display the game thing
app.get('/', (req, res) =>
    {
        if(!req.session.hasOwnProperty("loggedIn"))
        {
            req.session.loggedIn = false;
        }

        if(req.session.loggedIn)
        {
            res.write(fs.readFileSync("gamePage.html"));
        }
        else
        {
            res.write(fs.readFileSync("login.html"));
        }
        res.end();
    });

// end routes //



//launch express server
app.use(express.static('img'));
app.listen(port, () =>
    {
        console.log('Express server listening on port ' + port);
    });
