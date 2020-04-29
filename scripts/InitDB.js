var quotes = [
    {
        id: 1,
        quote: "Imagination is more important than knowledge. Knowledge is limited. Imagination encircles the world"
    },
    {
        id: 2,
        quote: "Try not to become a man of success, but rather try to become a man of value"
    },
    {
        id: 3,
        quote: "Life is like riding a bicycle. To keep your balance you must keep moving"
    },
    {
        id: 4,
        quote: "Look deep into nature, and then you will understand everything better"
    },
    {
        id: 5,
        quote: "Logic will get you from A to B. Imagination will take you everywhere"
    },
    {
        id: 6,
        quote: "Insanity is doing the same thing over and over again and expecting different results"
    },
    {
        id: 7,
        quote: "The hardest thing to understand in the world is the income tax"
    }
]

db = db.getSiblingDB('quotesdb');

quotes.map(function(item){
    print("Inserting:", item.id, item.quote)
    db.quotes.insertOne(item)
})
