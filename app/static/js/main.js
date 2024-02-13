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
    if (!subreddit) return; // If no subreddit is selected, do nothing

    $('#postList').empty(); // Clear existing posts

    $.get('/get_posts/' + subreddit, function(posts) {
        posts.forEach(function(post) {
            $('#postList').append($('<li>')
                                   .text(post.title)
                                   .attr('data-id', post.id)
                                   .click(function() {
                                       loadComments($(this).data('id'));
                                   }));
        });
    });
}
function loadComments(postId) {
    $('#commentSection').empty();
    $('#sentimentCounts').empty();
    $('#topWords').empty();
    $('#topWords').append('<ul></ul>'); // Add an unordered list element

    $.get('/get_comments/' + postId, function(data) {
        var sentiments = data.sentiment_counts;
        var countsText = 'Positive: ' + sentiments.positive + ', Neutral: ' + sentiments.neutral + ', Negative: ' + sentiments.negative;
        $('#sentimentCounts').text(countsText);

        data.top_words.forEach(function(word) {
            // Optionally capitalize the first letter of each word
            var capitalizedWord = word.charAt(0).toUpperCase() + word.slice(1);
            $('#topWords ul').append('<li>' + capitalizedWord + '</li>');
        });
    });
}


