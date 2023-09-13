const app = express();

const port = 3000;

app.get(url, function (req, res) {
    switch (url) {
        case "/":
            res.sendfile('index.html');
            res.writeHead(200, { "Content-Type": "text/plain" });
            console.log("Client requested /");
            break;
        case "/history":
            res.sendfile('index_history.html');
            res.writeHead(200, { "Content-Type": "text/plain" });
            console.log("Client requested /profile");
            break;
        default:
            res.sendfile('404.html');
            res.writeHead(404, { "Content-Type": "text/plain" });
            console.log("Client requested page not found - 404 error");
    }
});