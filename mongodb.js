use td;
db.dropDatabase();

// Insert some soccer players with a first name, last name, birthdate, height in kg, weight in cm and their position.
db.players.insertMany([
{
    firstName: "Lionel",
    lastName: "Messi",
    birthdate: new Date("1987-06-24"),
    height: 170,
    weight: 72,
    position: "forward"
},
{
    firstName: "Samuel",
    lastName: "Umtiti",
    birthdate: new Date("1993-11-14"),
    height: 182,
    weight: 75,
    position: "defender"
},
{
    firstName: "Marc-André",
    lastName: "Ter Stegen",
    birthdate: new Date("1992-04-30"),
    height: 187,
    weight: 85,
    position: "goal"
},
{
    firstName: "Blaise",
    lastName: "Matuidi",
    birthdate: new Date("1987-04-09"),
    height: 180,
    weight: 75,
    position: "midfield"
},
{
    firstName: "Christiano",
    lastName: "Ronaldo",
    birthdate: new Date("1985-02-05"),
    height: 187,
    weight: 83,
    position: "forward"
},
{
    firstName: "Gianluigi",
    lastName: "Buffon",
    birthdate: new Date("1978-01-28"),
    height: 192,
    weight: 92,
    position: "goal"
},
{
    firstName: "Kylian",
    lastName: "Mbappé",
    birthdate: new Date("1998-12-20"),
    height: 178,
    weight: 78,
    position: "forward"
},
{
    firstName: "Christian",
    lastName: "Früchtl",
    birthdate: new Date("2000-01-28"),
    height: 193,
    weight: 71,
    position: "goal"
},
{
    firstName: "Mats",
    lastName: "Hummels",
    birthdate: new Date("1988-12-16"),
    height: 191,
    weight: 92,
    position: "defender"
},
]);

// Create an index on the pair (first name, last name) to allow for faster search by name.
db.players.createIndex({"firstName": 1, "lastName": 1});

// Insert some soccer teams with some players.
db.teams.insertMany([
{
    name: "FC Barcelona",
    colors: ["Blue", "Red", "Maroon"],
    stadium: "Camp Nou",
    players: [{firstName: "Marc-André", lastName: "Ter Stegen"},
              {firstName: "Lionel", lastName: "Messi"},
              {firstName: "Samuel", lastName: "Umtiti"}]
},
{
    name: "FC Bayern Munich",
    colors: ["White", "Red"],
    stadium: "Allianz Arena",
    players: [{firstName: "Christian", lastName: "Früchtl"},
              {firstName: "Mats", lastName: "Hummels"}]
},
{
    name: "Juventus F.C.",
    colors: ["Black", "White"],
    stadium: "Allianz Stadium",
    players: [{firstName: "Blaise", lastName: "Matuidi"},
              {firstName: "Christiano", lastName: "Ronaldo"}]
},
{
    name: "Real Madrid C.F.",
    colors: ["White"],
    stadium: "Santiago Bernabéu Stadium",
    players: []
},
{
    name: "Paris Saint-Germain F.C.",
    colors: ["White", "Red", "Blue"],
    stadium: "Parc des Princes",
    players: [{firstName: "Gianluigi", lastName: "Buffon"},
              {firstName: "Kylian", lastName: "Mbappé"}]
}
]);

// Create an index on the team name.
db.teams.ensureIndex({"name": 1});

// Create some matches with two lists of players corresponding to the opposing teams. 
// Each player is given a rating between 0 and 10 for the match.
db.matches.insertMany([
{
    championship: "International Champions Cup",
    homeTeam: "Juventus F.C.",
    awayTeam: "FC Barcelona",
    homeScore: 1,
    awayScore: 2,
    homePlayers: [{firstName: "Juan", lastName: "Cuadrado", score: 3.39},
                  {firstName: "Blaise", lastName: "Matuidi", score: 9.95},
                  {firstName: "Daniele", lastName: "Rugani", score: 2},
                  {firstName: "Christiano", lastName: "Ronaldo", score: 7.98}],
    awayPlayers: [{firstName: "Lionel", lastName: "Messi", score: 9.51},
                  {firstName: "Sergi", lastName: "Roberto", score: 2.2},
                  {firstName: "Arda", lastName: "Turan", score: 3.69},
                  {firstName: "Samuel", lastName: "Umtiti", score: 5.48}],
},
{
    championship: "Champions League",
    homeTeam: "FC Barcelona",
    awayTeam: "FC Bayern Munich",
    homeScore: 3,
    awayScore: 0,
    homePlayers: [{firstName: "Marc-André", lastName: "Ter Stegen", score: 8.55},
                  {firstName: "Lionel", lastName: "Messi", score: 9.77},
                  {firstName: "Samuel", lastName: "Umtiti", score: 2.78},
                  {firstName: "Claudio", lastName: "Bravo", score: 2.75}],
    awayPlayers: [{firstName: "Pepe", lastName: "Reina", score: 4.21},
                  {firstName: "Mats", lastName: "Hammels", score: 3.07},
                  {firstName: "Claudio", lastName: "Pizarro", score: 9.72},
                  {firstName: "Gianluca", lastName: "Gaudino", score: 2.83}],
},
{
    championship: "Champions League",
    homeTeam: "Paris Saint-Germain F.C.",
    awayTeam: "FC Barcelona",
    homeScore: 4,
    awayScore: 0,
    homePlayers: [{firstName: "Gianluigi", lastName: "Buffon", score: 8.37},
                  {firstName: "Kylian", lastName: "Mbappé", score: 6.18},
                  {firstName: "Serge", lastName: "Aurier", score: 2.05},
                  {firstName: "Lucas", lastName: "Moura", score: 9.84}],
    awayPlayers: [{firstName: "Lucas", lastName: "Digne", score: 7.24},
                  {firstName: "Lionel", lastName: "Messi", score: 3.01},
                  {firstName: "Samuel", lastName: "Umtiti", score: 2.49},
                  {firstName: "Jasper", lastName: "Cillessen", score: 9.46}],
},
]);

// Find all the goalkeepers who are at most 25 years old.
db.players.find({
    position: "goal", 
    $expr: {$lte: [
        {$divide: [{$subtract: [new Date(), "$birthdate"]}, 31556952000]}, 
        25
    ]}
}).pretty();

// Store all the players who appear in a match in a single document.
// Count them and keep the ones who have played at least 3 matches.
// Compute for every player their average score in a new field 'score'.
db.matches.aggregate([{
	$project: { 
		player: {$concatArrays: ["$homePlayers", "$awayPlayers"]}
	}}, {
		$unwind: "$player"
	}, { 
		$group: {
			_id: {firstName: "$player.firstName", lastName: "$player.lastName"},
		        count: {$sum: 1},
			score: {$avg: "$player.score"}
		}
	}, {
		$match: {
			count: {$gte: 3}
		}
	}
]).pretty();
