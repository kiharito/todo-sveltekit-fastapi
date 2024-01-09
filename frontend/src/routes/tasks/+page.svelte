<script>
	let data = fetchTasks();

	async function fetchTasks() {
		const res = await fetch('http://127.0.0.1:8000/tasks/');
		const json = await res.json();

		if (res.ok) {
			return json;
		} else {
			throw new Error('Fetch Failed');
		}
	}
</script>

<div>
	<p>Task List</p>
	{#await data}
		<p>Loading...</p>
	{:then tasks}
		<ul>
			{#each tasks as task (task.id)}
				<li>{task.title}</li>
			{/each}
		</ul>
	{:catch error}
		<p>{error.message}</p>
	{/await}
</div>
