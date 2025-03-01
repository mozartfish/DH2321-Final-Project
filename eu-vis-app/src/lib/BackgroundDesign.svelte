<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VIS Main Page</title>
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

        /* Top bar: Title + Image */
        .top-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
        }

        .image-box {
						margin-left: 20px;
            width: 40px;
            height: 40px;
            background: rgba(255, 255, 255, 0.3);
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 50px;
            flex-shrink: 0;
						font-size: 30px;
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

        /* Top row: EU Heatmap + Two charts */
        .top-content {
            display: flex;
            flex: 1;
            gap: 20px;
            width: 100%;
        }

        .eu-heatmap {
            background: rgba(49, 53, 110, 0.3);
            border-radius: 10px;
            display: flex;
						flex: 2; /* Adjust map container size */
            justify-content: center;
            align-items: center;
            font-size: 200px;
            height: 100%;
        }

        .charts {
            display: flex;
            flex-direction: column;
            flex: 1;
            gap: 20px;
            height: 100%;
        }

        .chart {
            background: rgba(65, 184, 213, 0.1);
            border-radius: 10px;
            display: flex;
						flex: 1;
            justify-content: center;
            align-items: center;
            font-size: 50px;
        }

        /* Line Graph Container */
        .linegraph {
            background: rgba(49, 53, 110, 0.3);
            border-radius: 10px;
            font-size: 200px;
            display: flex;
						flex: 1; 
            justify-content: center;
            align-items: center;
            width: 100%;
            
        }

        /* Policy Boxes */
        .policy-boxes {
            display: flex;
						flex: 1;
            gap: 20px;
            width: 100%;
            
        }

        .country-policy {
	        background: rgba(65, 184, 213, 0.1);
            border-radius: 10px;
            display: flex;
			flex: 1;
            justify-content: center;
            align-items: center;
            font-size: 20px;
        }

        .menu-icon img {
            width: 25px;  /* Adjust as needed */
            height: 25px;
            object-fit: contain; /* Ensures the image maintains aspect ratio */
            cursor: pointer;
        }

    </style>
</head>
	
<body>

    <!-- Sidebar Menu -->
    <div class="sidebar-menu">
        <div class="menu-icon"><img src="src/icons/global.png" alt="Menu"></div>
        <div class="menu-icon"><img src="src/icons/menu.png" alt="Home"></div>
        <div class="menu-icon"><img src="src/icons/group.png" alt="Charts"></div>
    </div>

    <!-- Page Title and Flag Image -->
    <div class="main-container">
        <div class="top-bar">
            <div class="title">EU Climate Insights</div>
            <div class="image-box">🇪🇺</div>
        </div>

        <!-- Map, Bar Chart and Sunburst Chart -->
        <div class="page-content">
            <!-- Top Row: Large Map Box + Two Small Chart Boxes -->
            <div class="top-content">
                <div class="eu-heatmap">🌍</div>
                <div class="charts">
                    <div class="chart">📊</div>
                    <div class="chart">☀️</div>
                </div>
            </div>

            <!-- Linegraph Container-->
            <div class="linegraph">📈</div>           

            <!-- Policy Information Containers -->
            <div class="policy-boxes">
                <div class="country-policy">Country Policy Info</div>
                <div class="country-policy">Country Policy Info</div>
            </div>
        </div>
    </div>

</body>
</html>
