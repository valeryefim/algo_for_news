<!DOCTYPE html>
<html>
<head>
    <title>Interesting Articles</title>
    <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
</head>
<body>
    <div class="ui container" style="padding-top: 10px;">
        <h1>Возможно, вам понравятся эти статьи</h1>
        <table class="ui celled table">
            <thead>
                <th>Статьи</th>
            </thead>
            <tbody>
                %for row in rows:
                <tr>
                    <td><a href="{{ row.url }}">{{ row.title }}</a></td>
                </tr>
                %end
            </tbody>
        </table>
    </div>
</body>
</html>