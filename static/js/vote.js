function handle_vote(event) {
	// Prevent default action from pressing button
	event.preventDefault();

	const button = event.currentTarget;
	const form = button.parentNode;
	const card = form.parentNode.parentNode;

	// Check if thread vote exists
	const is_upvoted = card.querySelector(".upvote-form > button > img").classList.contains('bg-yellow');
	const is_downvoted = card.querySelector(".downvote-form > button > img").classList.contains('bg-yellow');

	// Check if the action is an upvote or downvote, based on url
	const is_upvote = form.action.includes('upvote');
	const is_downvote = form.action.includes('downvote');

	// getting Form data, send form as http request
	fetch(form.action, { method: 'POST', body: new FormData(form) })
	.then((res) => {
		// get vote and arrow img to update later
		const image = button.querySelector('img');
		const vote_count = card.querySelector('.vote-count');

		// remove all old yellow backgrounds
		card.querySelectorAll(".vote-form > button > img").forEach(img => img.classList.remove('circle', 'bg-yellow'));

		// Add yellow background if voted
		if (!((is_upvote && is_upvoted) || (is_downvote && is_downvoted))) {
			image.classList.add('circle', 'bg-yellow');
		}

		// Adjust Vote count
		if(is_upvote) {
			if(is_upvoted) {
				vote_count.innerHTML = Number(vote_count.innerHTML) - 1;
			} else if(is_downvoted) {
				vote_count.innerHTML = Number(vote_count.innerHTML) + 2;
			} else {
				vote_count.innerHTML = Number(vote_count.innerHTML) + 1;
			}
		} else if(is_downvote) {
			if(is_downvoted) {
				vote_count.innerHTML = Number(vote_count.innerHTML) + 1;
			} else if(is_upvoted) {
				vote_count.innerHTML = Number(vote_count.innerHTML) - 2;
			} else {
				vote_count.innerHTML = Number(vote_count.innerHTML) - 1;
			}
		}

	})
	.catch(() => {
		console.log('error');
	});
}

document.addEventListener("DOMContentLoaded", () => {
	const vote_buttons = document.querySelectorAll(".vote-form > button");
	vote_buttons.forEach(button => button.addEventListener("click", handle_vote));
});
