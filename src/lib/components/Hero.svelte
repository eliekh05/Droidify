<script>
let searchInput = '';
let loader = null;

async function handleSearch() {
    loader = true;
    if (searchInput.trim()) {
        // This would typically call an API to search for the device
        const data = await handleSubmit();
        // change the state of the of the loader to false
        loader = false
        // display the results in a div container or wrapper
        console.log(data)
    } else {
        alert('Please enter a device model to search');
    }
}

async function handleSubmit() {
    const response = await fetch(`/api/search/${searchInput}`)
    const data = await response.json()
    return data
}
</script>

<section class="hero" id="home">
    <div class="container">
        <h1>All Android Custom ROMs in One Place</h1>
        <p>Stop wasting days searching for custom firmware files. Our platform provides all the resources, tools, and guides you need for any Android device - ready to use in minutes, not days.</p>
        <div class="search-bar">
            <input type="text" bind:value={searchInput} placeholder="Enter your device model">
            <button on:click={handleSearch}><i class="fas fa-search"></i> Find Resources</button>
        </div>
    </div>
</section>

<style>
.hero {
background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1598327105666-5b89351aff97?ixlib=rb-1.2.1&auto=format&fit=crop&w=2000&q=80');
background-size: cover;
background-position: center;
color: white;
padding: 5rem 0;
text-align: center;
}

.hero h1 {
font-size: 3rem;
margin-bottom: 1.5rem;
}

.hero p {
font-size: 1.2rem;
margin-bottom: 2rem;
max-width: 800px;
margin-left: auto;
margin-right: auto;
}

.search-bar {
max-width: 600px;
margin: 0 auto;
display: flex;
}

.search-bar input {
flex: 1;
padding: 1rem;
border: none;
border-radius: 5px 0 0 5px;
font-size: 1rem;
}

.search-bar button {
background-color: var(--primary-color);
color: white;
border: none;
padding: 1rem 1.5rem;
border-radius: 0 5px 5px 0;
cursor: pointer;
transition: background-color 0.3s;
}

.search-bar button:hover {
background-color: #3367d6;
}

@media (max-width: 768px) {
.hero h1 {
font-size: 2.5rem;
}

.search-bar {
flex-direction: column;
}

.search-bar input {
border-radius: 5px;
margin-bottom: 1rem;
}

.search-bar button {
border-radius: 5px;
}
}
</style>
