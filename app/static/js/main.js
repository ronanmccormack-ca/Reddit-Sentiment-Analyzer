$(document).ready(function() {
    loadSubreddits();
});

function loadSubreddits() {
    $.get('/get_subreddits', function(data) {
        data.forEach(function(subreddit) {
            $('#subreddit').append($('<option>', {
                value: subreddit,
                text: subreddit
            }));
        });
    });
}
function loadPosts(subreddit) {
    $('#postList').empty(); // Clear existing posts

    $.get('/get_posts/' + subreddit, function(posts) {
        posts.forEach(function(post) {
            var listItem = $('<li>')
                .text(post.title)
                .attr('data-id', post.id)
                .click(function() {
                    var postId = $(this).data('id');
                    loadComments(postId);
                    loadTopWords(postId);
                });

            $('#postList').append(listItem);
        });
    });
}

function loadComments(postId) {
    $('#commentSection').empty();
    $('#sentimentCounts').empty();

    // Load comments and their sentiments
    $.get('/get_comments/' + postId, function(data) {
        var sentiments = data;
        var countsText = 'Positive: ' + sentiments.positive + ', Neutral: ' + sentiments.neutral + ', Negative: ' + sentiments.negative;
        $('#sentimentCounts').text(countsText);
    });
}

function loadTopWords(postId) {
    $('#topWords').empty();
    $('#topWords').append('<ul></ul>'); // Add an unordered list element

    // Load top phrases
    $.get('/get_top_phrases/' + postId + '/' + 2, function(topPhrases) {
        topPhrases.forEach(function(phrase) {
            // Capitalize the first letter of each phrase
            var capitalizedPhrase = phrase.split(' ').map(function(word) {
                return word.charAt(0).toUpperCase() + word.slice(1);
            }).join(' ');
            $('#topWords ul').append($('<li>').text(capitalizedPhrase));
        });
    });
}
