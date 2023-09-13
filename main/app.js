const express = require('express');

const mysql = require('mysql2');

const app = express();

const port = 3000;

const pool = mysql.createPool({
    connectionLimit: 10,
    host: '192.168.80.1',
    database: 'crawl_tiki_panther',
    user: 'root',
    port: '6603',
    password: '123456'
});

app.get('/', (request, response) => {

    response.sendFile(__dirname + '/index.html');

});

app.listen(port, () => {

    console.log(`Server listening on port ${port}`);

});

app.get('/search', (request, response) => {

    const query = request.query.q;

    var sql = '';

    if (query != '') {
        sql = `SELECT * FROM product_info WHERE ID_product LIKE '%${query}%' or Product_name LIKE '%${query}%'`;
    }
    else {
        sql = `SELECT * FROM product_info ORDER BY ID_product`;
    }

    pool.query(sql, (error, results) => {

        if (error) throw error;

        response.send(results);

    });

});

app.get('/a', (request, response) => {

    response.sendFile(__dirname + '/index_history.html');

});


app.get('/history', (request, response) => {

    sql = `SELECT * FROM history_crawl_data`;

    pool.query(sql, (error, results) => {

        if (error) throw error;

        response.send(results);

    });

});
