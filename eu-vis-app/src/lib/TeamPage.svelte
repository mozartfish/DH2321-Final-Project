<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Meet the Team</title>
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

			/* Page-settings, Gradient background */
        body {
			background: linear-gradient(to right, #001122, #001233);
            height: auto; 
			width: auto;
            display: auto;
            font-family: Figtree, sans-serif;
            color: white;
            
        }

        /* Sidebar (Fixed on the left) */
        .sidebar-menu {
			background: rgba(0, 0, 0, 0); /*Adjust here if we want color*/
            height: 100vh;
			width: 50px; /* Adjust width here */
			display: flex;
            flex-shrink: 0;
			flex-direction: column;
            align-items: center;
            padding-top: 20px;
            gap: 20px;
			position: fixed; /* This keeps it in place */ 
            left: 0;
            top: 0;
            
        }

        .menu-icon {
            background: rgba(255, 255, 255, 0);
			width: 20px;
            height: 20px;
            border-radius: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 24px;
            cursor: pointer;
        }

        /* Main container, holds all containers */
	      .main-container {
            margin-left: 50px;
            flex: 1;
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            gap: 20px;
        }

        /* Top bar: Title */
        .top-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
        }

        .title {
            font-size: 28px;
            font-weight: bold;
            white-space: nowrap;
        }

        /* Page content containers */
        .page-content {
            display: flex;
            flex-direction: column;
			flex: 1;
            gap: 20px;
            width: 100%;
        }

        .menu-icon img {
            width: 25px;  /* Adjust as needed */
            height: 25px;
            object-fit: contain; /* Ensures the image maintains aspect ratio */
            cursor: pointer;
        }

	.team-container {
    text-align: center;
    margin-top: 50px;
}

.team-grid {
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
}

.team-member {
    background: rgba(65, 184, 213, 0.1);
    border-radius: 10px;
    padding: 10px;
    text-align: center;
    width: 150px;
}

.team-member img {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 50%;
    border: 2px solid white;
}

.team-member p {
    margin-top: 10px;
    font-size: 14px;
}


    </style>
</head>
	
<body>

    <!-- Sidebar Menu -->
    <div class="sidebar-menu">
        <div class="menu-icon"><img src="src/assets/icons/global.png" alt="Home"></div>
        <div class="menu-icon"><img src="src/assets/icons/menu.png" alt="Info"></div>
        <div class="menu-icon"><img src="src/assets/icons/group.png" alt="Group"></div>
    </div>

    <!-- Page Title and Flag Image -->
    <div class="main-container">
        <div class="top-bar">
            <div class="title">Meet the Team</div>
        </div>
			
		<!-- Team Section -->
<div class="team-container">
    <div class="team-grid">
        <div class="team-member">
            <img src="src/assets/profiles/antonia.png" alt="Antonia">
            <p>Antonia</p>
        </div>
        <div class="team-member">
            <img src="src/assets/profiles/fanny.png" alt="Fanny">
            <p>Fanny</p>
        </div>
        <div class="team-member">
            <img src="src/assets/profiles/pranav.png" alt="Pranav">
            <p>Pranav</p>
        </div>
        <div class="team-member">
            <img src="src/assets/profiles/matei.png" alt="Matei">
            <p>Matei</p>
        </div>
        <div class="team-member">
            <img src="src/assets/profiles/safi.png" alt="Safi">
            <p>Safi</p>
        </div>
    </div>
</div>


</body>
</html>
