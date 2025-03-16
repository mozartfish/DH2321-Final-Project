<script>
  // Array of content sections
  const sections = [
    { id: 0, title: 'About the Project' },
    { id: 1, title: 'Walkthrough' },
    { id: 2, title: 'Technology' },
    { id: 3, title: 'Data' },
    { id: 4, title: 'Data Description' }
  ];

  // Track the current active section
  let currentSection = 0;

  // Function to change the active section
  function setActiveSection(id) {
    currentSection = id;
  }

  const videoId = 'ml8zxmAuw7M?si=6A86WE2aiMU258cv';
</script>

<main>
  <section class="container">
    <div class="tab-navigation">
      {#each sections as section}
        <button
          class="tab-button"
          class:active={currentSection === section.id}
          on:click={() => setActiveSection(section.id)}
        >
          {section.title}
        </button>
      {/each}
    </div>

    <!-- About the Project section -->
    <div class="content-box" class:active={currentSection === 0}>
      <h1>About the Project</h1>
      <p>
        Europe has long been at the forefront of the fight against climate
        change, pioneering policies that align with the <b
          >United Nations Sustainable Development Goals (SDGs)</b
        >. The SDGs play a crucial role in ensuring that economic growth does
        not come at the cost of planetary health. Yet, despite ambitious goals
        and <b>policy frameworks like the European Green Deal</b>, data shows
        that many environmental boundaries are still being transgressed.
      </p>
      <p>
        This project uses interactive visualizations to tell the story of
        Europe's sustainability progress and challenges, helping policymakers,
        researchers, and the public grasp the real impact of consumption and
        climate action.
      </p>
      <p>
        Our goal is to create a data-driven, interactive storytelling platform
        that can be used to visualize:
      </p>
      <ul>
        <li>
          How Europe and its member states are progressing towards sustainable
          consumption and climate goals.
        </li>
        <li>
          The extent to which consumption impacts have exceeded planetary
          boundaries.
        </li>
        <li>
          The role of policy measures (e.g., energy taxes, carbon pricing) in
          steering Europe towards sustainability.
        </li>
      </ul>

      <p>
        A clear before-and-after perspective, showing changes over time. Climate
        change is not just an environmental issue—it's an economic, political,
        and social challenge. By translating complex climate data into engaging
        visualizations, we aim to make sustainability challenges more
        understandable and actionable. Europe's journey towards the SDGs is far
        from over—but with data, visualization, and informed action, we can
        hopefully inspire and potentially help make change.
      </p>

      <hr>

      <h3>References</h3>
      <p>European Commission. (2020). The European Green Deal. Retrieved 21 February, 2025, from 
          <a href="https://commission.europa.eu/strategy-and-policy/priorities-2019-2024/european-green-deal_en">https://commission.europa.eu/strategy-and-policy/priorities-2019-2024/european-green-deal_en</a>
      </p>
      <p>Eurostat. (2022). Eurostat. Retrieved 21 february, 2025 from 
          <a href="https://ec.europa.eu/eurostat">https://ec.europa.eu/eurostat</a>
      </p>
      <p>Eurostat. (2021). Eurostat metadata. Retrieved 21 february, 2025, from 
          <a href="https://ec.europa.eu/eurostat/web/metadata/overview">https://ec.europa.eu/eurostat/web/metadata/overview</a>
      </p>
  
      <p>United Nations. (2025). Sustainable development goals. United Nations Department of Economic and Social Affairs. Retrieved 21 february, 2025, from 
          <a href="https://sdgs.un.org/goals">https://sdgs.un.org/goals</a>
      </p>

    </div>

    <!-- Walkthrough section -->
    <div class="content-box" class:active={currentSection === 1}>
      <h2>Walkthrough</h2>
      <ul>
        <li><b>The Big Picture</b></li>
        <ul>
          <li>
            A heatmap of EU countries comparing observed values in climate data
            to other countries in the EU.
          </li>
          <li>
            A time slider to see changes and policy implementations over time.
          </li>
          <li>
            A bar chart that shows how countries perform on climate issues in relationship to other EU countries. The observed values have been statistically transformed into z-scores. The mean of how EU is doing on a climate issue is indicated by the mid line. A negative score indicates that the observed values are below the average of all EU countries, whereas a positive score signifies that they exceed the EU average.
          </li>
          <li>
            A line chart that shows how countries compare to other countries and
            the total of EU on climate data.
          </li>
          <li>
            A policy chart that visualizes enacted policies in total or in
            sectors by year.
          </li>
          <li>A text box that lists enacted policies.</li>

          <div class="video-container">
            <div class="video-wrapper">
              <h3 class="video-title">Demo video</h3>
              <iframe
                width="700"
                height="400"
                src="https://www.youtube.com/embed/{videoId}"
                title="Demo video"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
              >
              </iframe>
            </div>
          </div>
        </ul>
        <li>
          <b>Climate Challenges: What Challenges do Specific Countries Face?</b>
        </li>
        <ul>
          <li>
            The bar chart shows climate data in relation to the average of all
            EU countries (indicated by the midline). A score of -1 to 0 means
            that the country's observed values are comparatively smaller than
            the average of the EU. A score of 0 to 1 means that the countries
            observed values are comparatively larger than the average of the EU.
          </li>
        </ul>
        <li><b>The Policy Impact: What's Working, What's Not?</b></li>
        <ul>
          <li>
            A donut chart visualizing the number of enacted policies in total
            and within different sectors by year. A more detailed list of the
            implemented policies will be updated on selection.
          </li>
        </ul>
      </ul>
      <h3>Quick Tips</h3>
      <ul>
        <li>Select a country on the map view to enter a detailed view.</li>
        <li>
          Select multiple countries at once in the detailed view to compare
          against EU data or other countries.
        </li>
        <li>The map data will update the bar chart and the line chart.</li>
        <li>
          Use the time slider on the bottom to change the year of the data you
          are viewing.
        </li>
        <li>
          Click on specific climate data in the bar chart to see how different
          countries compare in the map and line chart.
        </li>
        <li>
          Hover over the lines in the line chart or click on a country in the
          legend to see a specific country in more detail. If you want to filter
          out and look more closely at specific countries, use the map. If you
          want to inspect other climate data, select in the bar chart.
        </li>
        <li>
          Hover over a sector within the donut chart to view the number of
          implemented policies, and click on a sector to show policies for that
          sector, displayed below.
        </li>
        <li>
          Select the RESET button under the map to reset the map filtering.
        </li>
        <li>
          Select the RESET button under the policy chart to reset the policy
          chart and list.
        </li>
      </ul>
    </div>

    <!-- Technology section -->
    <div class="content-box" class:active={currentSection === 2}>
      <h2>Technology</h2>
      <p>These visualizations have been built using:</p>
      <ul>
        <li><b>Data Processing:</b> R, Python, CSV, JSON files</li>
        <li><b>Web Development:</b> Svelte, D3.js</li>
        <li><b>Design:</b> Figma</li>
      </ul>
    </div>

    <!-- Data section -->
    <div class="content-box" class:active={currentSection === 3}>
      <h2>Data</h2>

      <h3>Data Types</h3>
      <ul>
        <li>Ordinal (Year)</li>
        <li>Categorical (Country)</li>
        <li>Categorical (Policies, Categorized Groups)</li>
        <li>Quantitative (Percentages, Ratios, Observations)</li>
      </ul>

      <h3>Tasks</h3>
      <ul>
        <li>Analyze: Discover</li>
        <li>Search: Browse & Explore</li>
        <li>Query: Identify & Compare</li>
        <li>Target: Find extremes & Trends</li>
      </ul>

      <hr>

      <h3> Original Data Source</h3>
      <li><a href="https://ec.europa.eu/eurostat/web/sdi/database"
        >Eurostat SDG Database</a> </li>
      <li><a href="https://international-partnerships.ec.europa.eu/policies_en"
        >European Commission Policies</a> </li>

      <h3> Processed data: </h3>
       <li> <a href="https://github.com/mozartfish/DH2321-Final-Project/tree/eu-climate-policy-vis/data1"
        >Eurostat SDG Database</a> </li>
       <li><a href="https://github.com/mozartfish/DH2321-Final-Project/blob/eu-climate-policy-vis/policies.csv"
        >European Commission Policies</a> </li> 
      <p class="link"></p>
      
    </div>

    <!-- Data description section -->
    <div
      class="content-box data-description"
      class:active={currentSection === 4}
    >
      <h2>Data</h2>
      <h3>Industry Emissions</h3>
      <p>
        This indicator tracks the emissions intensity of particulate matter
        (PM10 and PM2.5) from the manufacturing sector (NACE Rev. 2 sector ‘C’).
        PM10 includes particles under 10 micrometers, which can reach deep into
        the lungs, worsening heart and lung conditions. PM2.5, a finer subset
        under 2.5 micrometers, poses even greater health risks as it penetrates
        further and may be more toxic. Emission intensity is calculated by
        dividing the sector’s PM emissions by its gross value added (GVA), which
        represents output minus intermediate consumption.
      </p>
      <p>
        <b>Unit of Measure:</b> Grams per euro, chain-linked volumes (2010).
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/de/sdg_09_70_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />

      <h3>Soil Erosion</h3>
      <p>
        This indicator estimates the area at high risk of severe soil erosion by
        water (e.g., rain splash, sheet-wash, and rills), defined as soil loss
        exceeding 10 tonnes per hectare per year. The affected area is measured
        in km² and as a percentage of the country’s non-artificial, erodible
        land. Countries with no land exceeding this erosion threshold receive a
        value of zero, though lower rates of erosion may still occur.
      </p>
      <p>
        Estimates are based on a modified RUSLE 2015 model, using 100 m
        resolution data and peer-reviewed input layers, including rainfall
        erosivity, soil erodibility, topography, land use, and management. The
        analysis includes agricultural and forested areas but excludes
        artificial, sandy, rocky, icy, wetland, and water surfaces.
      </p>
      <p>
        <b>Unit of Measure:</b> km2 and % of the non-artificial erodible area.
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/fr/sdg_15_50_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />

      <h3>Car Co2</h3>
      <p>
        This indicator measures the average carbon dioxide (CO2) emissions per
        km from new passenger cars each year. The reported values are based on
        type-approval tests, which may differ from actual emissions. Until 2019,
        emissions were measured using the ‘New European Driving Cycle’ (NEDC).
        In 2020, both NEDC and the ‘Worldwide Harmonized Light Vehicles Test
        Procedure’ (WLTP) were used, and from 2021 onward, only WLTP data is
        reported.
      </p>
      <p>
        <b>Unit of Measure:</b>g CO2 per km.
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/en/sdg_13_31_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />

      <h3>Bathing Quality</h3>
      <p>
        This indicator measures the percentage of inland and coastal bathing
        sites in the EU with excellent water quality. Quality is assessed based
        on microbiological standards for intestinal Enterococci and Escherichia
        coli, using a moving average of at least 16 sampling events over four
        years to ensure reliable classification. Under the Bathing Water
        Directive (BWD), Member States must monitor and classify bathing waters
        as poor, sufficient, good, or excellent, based on detected levels of
        faecal bacteria.
      </p>
      <p>
        <b>Unit of Measure:</b> Number and percentage of bathing sites with
        excellent water quality (i. Coastal water, ii. Inland water).
        <a
          href=" https://ec.europa.eu/eurostat/cache/metadata/en/sdg_14_40_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />

      <h3>River BOD</h3>
      <p>
        This indicator tracks biochemical oxygen demand (BOD) in rivers,
        measuring the oxygen required by microorganisms to decompose organic
        matter. BOD is a key water quality indicator, showing temporal trends
        and geographic variations in nutrient concentrations. BOD5 (oxygen
        demand over five days at 20°C) is measured in mg O₂/L, weighted by the
        number of monitoring stations. High BOD5 values indicate organic
        pollution:
      </p>
      <ul>
        <li>Clean rivers: BOD5 &gt; 1 mg O₂/L</li>
        <li>Moderately to heavily polluted rivers: BOD5 = 2–8 mg O₂/L</li>
      </ul>
      <p>
        <b>Unit of Measure:</b> mg O2 per litre.
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/en/sdg_06_30_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />

      <h3>Material Use</h3>
      <p>
        The circular material use rate measures the share of recycled materials
        fed back into the economy, reducing the need for extracting primary raw
        materials. It is calculated as the ratio of recycled waste to total
        material use, including domestic material consumption (DMC) and waste
        recovered through recycling. A higher circularity rate indicates greater
        resource efficiency and lower environmental impact.
      </p>
      <p>
        <b>Unit of Measure:</b> Percentage of total material use.
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/en/cei_srm030_esmsip2.htm "
          >Source</a
        >
      </p>
      <hr />

      <h3>Climate Losses</h3>
      <p>
        The economic losses from weather and climate-related events indicator
        tracks financial damages caused by storms, floods, heatwaves, droughts,
        and other extreme events, as classified by the International Council for
        Science (ICSU). Data includes annual figures and 30-year averages to
        show long-term trends while minimizing short-term climate variability.
        The indicator is based on CATDAT data from RiskLayer.
      </p>
      <p>
        <b>Unit of Measure:</b> Million EUR and EUR per capita (2022 constant
        prices).
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/en/sdg_13_40_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />

      <p><b>Consumption Footprint </b></p>
      <p>
        The Consumption Footprint (CF) measures the environmental impact of EU
        consumption using 16 life cycle assessment (LCA)-based indicators. It
        evaluates emissions, resource use, and consumption intensity across
        food, mobility, housing, household goods, and appliances. CF indicators
        compare impacts to Planetary Boundaries, showing how consumption exceeds
        sustainable limits.
      </p>
      <p>
        <b>Unit of Measure:</b> Planetary boundaries and per inhabitant.
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/en/sdg_12_31_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />
      <h3>Climate Finance</h3>
      <p>
        The climate finance indicator tracks the total annual spending by EU
        Member States, the European Commission, and the European Investment Bank
        toward the UNFCCC’s $100 billion climate finance commitment. Data covers
        multilateral and bilateral public finance commitments for 2020–2021, and
        from 2022 onwards, it includes bilateral finance commitments and
        multilateral finance provided.
      </p>
      <p>
        <b>Unit of Measure:</b> Million EUR (current prices) and EUR per capita.
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/en/sdg_13_50_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />

      <h3>Drought Impact</h3>
      <p>
        The drought impact indicator measures the area affected by agricultural
        droughts, tracking vegetation productivity decline due to severe soil
        moisture deficits during the growing season. It is based on remote
        sensing data (500×500 m resolution) from the Copernicus EMS European
        Drought Observatory. This indicator focuses on agricultural droughts
        caused by insufficient precipitation, unlike hydrological droughts,
        which affect water bodies over longer periods.
      </p>
      <p>
        <b>Unit of Measure:</b> Km2 area affected % of total area.
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/en/sdg_15_42_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />

      <h3>Energy Productivity</h3>
      <p>
        Energy productivity measures GDP per unit of energy consumed, indicating
        how efficiently energy is used in economic production. Chain-linked
        volumes are used for comparisons over time within a country, while
        Purchasing Power Standard (PPS) values allow cross-country comparisons
        for a specific year.
      </p>
      <p>
        <b>Unit of Measure:</b> [EUR_KGOE] Euro per kilogram of oil equivalent
        (KGOE) [PPS_KGOE] Purchasing power standard (PPS) per kilogram of oil
        equivalent.
        <a
          href=" https://ec.europa.eu/eurostat/cache/metadata/en/nrg_ind_ep_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />

      <h3>Waste Generation</h3>
      <p>
        The waste statistics indicator tracks waste generation and treatment in
        EU Member States under Regulation (EC) No. 2150/2002. Data is collected
        on: * Waste generation by 19 business sectors (NACE classification) and
        households, * Waste treatment by five methods (recovery, incineration
        with/without energy recovery, landfill, and land treatment), * Waste
        categories (European Waste Classification). Values are reported in
        tonnes and kg per capita. Member States choose their data collection
        methods (surveys, administrative sources, or estimates). Some early data
        (2004) may be incomplete due to exemptions.
      </p>
      <p>
        <b>Unit of Measure:</b> 1) Tonnes (European totals are rounded to 10,000
        tonnes for confidentiality reasons) 2) kg per capita (based on the
        annual average of the population).
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/en/env_wasgt_esms.htm"
          >Source</a
        >
      </p>
      <hr />

      <h3>Environmental Value</h3>
      <p>
        The Environmental Goods and Services Sector (EGSS) includes businesses
        that produce goods and services for environmental protection and
        resource management, both domestically and internationally. Its gross
        value added (GVA) represents its contribution to GDP, calculated as the
        difference between the sector’s output and intermediate consumption.
      </p>
      <p>
        <b>Unit of Measure:</b> 1) Chain linked volumes (2010) in EUR 2) % of
        GDP.
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/en/sdg_12_61_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />

      <h3>GHG Emissions</h3>
      <p>
        The greenhouse gas (GHG) emissions indicator tracks total national
        emissions, including international aviation, from all sectors covered in
        GHG inventories. It includes CO₂, CH₄, N₂O, and F-gases and is measured
        in CO₂ equivalents using global warming potential (GWP). Emissions are
        reported with and without land use, land use change, and forestry
        (LULUCF). Data is submitted annually by EU Member States to the UNFCCC,
        following IPCC guidelines to ensure transparency and consistency.
      </p>
      <p>
        <b>Unit of Measure:</b> Index 1990 = 100 and tonnes of CO2 equivalent
        per capita.
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/en/sdg_13_10_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />

      <h3>Groundwater Nitrate</h3>
      <p>
        The nitrate concentration in groundwater indicator measures NO₃ levels
        (mg/L) in European groundwater bodies using annual averages from well
        samples. It highlights geographical variations and temporal trends in
        nutrient pollution, mainly from agricultural sources. Nitrate can
        persist in groundwater, and the EU drinking water standard is 50 mg
        NO₃/L to protect human health. Data covers 1016 groundwater bodies (958
        in 18 EU Member States) for 2000–2022, with recalculations due to
        changes in monitoring stations. The EU_V aggregate includes data from 18
        EU countries.
      </p>
      <p>
        <b>Unit of Measure:</b> Mg NO3 per litre.
        <a href="https://ec.europa.eu/eurostat/cache/metadata/en/sdg_06_4 "
          >Source</a
        >
      </p>
      <hr />

      <h3>Rivers Phosphate</h3>
      <p>
        The phosphate concentration in rivers indicator measures dissolved PO₄
        levels (mg/L) in water samples, aggregated into annual averages. High
        phosphate levels can lead to eutrophication, causing excessive growth of
        algae and macrophytes, which impacts water quality. Data covers 669
        monitoring sites (581 in 15 EU Member States) for 2000–2022. Since
        monitoring stations change over time, the indicator is recalculated with
        each update. The EU_V aggregate includes data from 15 EU countries.
      </p>
      <p>
        <b>Unit of Measure:</b> Mg PO4 per litre.
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/fr/sdg_06_50_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />

      <h3>Energy Use</h3>
      <p>
        The primary energy consumption indicator measures a country's total
        energy demand, excluding non-energy uses (e.g., natural gas for chemical
        production). It includes:
      </p>
      <ul>
        <li>
          Final energy consumption (industry, transport, households, services,
          and agriculture)
        </li>
        <li>
          Energy sector consumption (for energy production and transformation)
        </li>
        <li>Transformation losses (e.g., electricity generation efficiency)</li>
        <li>Transmission and distribution losses</li>
      </ul>
      <p>
        This provides a comprehensive view of national energy use and
        efficiency.
      </p>
      <p>
        <b>Unit of Measure:</b> Million tonnes of oil equivalent (TOE), index
        2005 = 100 and TOE per capita.
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/de/sdg_07_10_esmsip2.htm "
          >Source</a
        >
      </p>
      <hr />

      <h3>Material Consumption</h3>
      <p>
        Material footprint (Raw Material Consumption - RMC) measures the global
        material demand driven by a region's consumption of goods and services.
        It includes domestic extraction (minerals, metals, biomass, fossil
        fuels) and the raw material equivalents of imports and exports,
        reflecting the total material required for production, regardless of
        where extraction occurs. Data is based on material flow accounts.
      </p>
      <p>
        <b>Unit of Measure:</b> Thousand tonnes and tonnes per capita.
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/en/sdg_12_21_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />

      <h3>Renewable Share</h3>
      <p>
        The renewable energy share indicator measures the percentage of
        renewable energy in gross final energy consumption, as defined by the
        Renewable Energy Directive. Gross final energy consumption includes
        end-user consumption, grid losses, and power plant self-consumption.
      </p>
      <p>
        <b>Unit of Measure:</b> % by sectors.
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/en/sdg_07_40_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />

      <h3>Water Exploitation</h3>
      <p>
        The regionalised Water Exploitation Index (WEI+) measures total water
        consumption as a percentage of renewable freshwater resources in a given
        area and period. It accounts for water abstraction and returns, with
        consumption being the difference.
      </p>
      <ul>
        <li>WEI+ > 20% indicates water scarcity</li>
        <li>WEI+ ≥ 40% signals severe, unsustainable water use</li>
      </ul>
      <p>
        Annual national WEI+ may mask seasonal and regional water stress. When
        reported data is insufficient, the EEA applies model-based estimates
        using multiple data sources.
      </p>
      <p>
        <b>Unit of Measure:</b> % of renewable freshwater resources.
        <a
          href="https://ec.europa.eu/eurostat/cache/metadata/en/sdg_06_60_esmsip2.htm"
          >Source</a
        >
      </p>
      <hr />

      <h3>Soil Sealing</h3>
      <p>
        The soil sealing indicator measures the increase in impervious surfaces
        due to urban development and construction (e.g., buildings, roads, and
        artificial materials like asphalt and concrete). It tracks the rate of
        soil sealing as land use shifts to urban areas. Data comes from the
        Copernicus Land Monitoring Service (imperviousness High Resolution
        Layer).
      </p>
      <p>
        <b>Unit of Measure:</b> Index 2006=100 % of total surface total sealed
        surface in km2.
        <a
          href="https://ec.europa.eu/eurostat/databrowser/view/sdg_15_41/default/table"
          >Source</a
        >
      </p>
    </div>
  </section>
</main>

<style>
  .container {
    margin: 0 auto;
    padding: 60px 20px;
    max-width: 1200px;
  }

  .tab-navigation {
    display: flex;
    justify-content: center;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 20px;
    flex-wrap: wrap;
  }

  .tab-button {
    background: none;
    border: none;
    padding: 15px 20px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    color: #555;
    font-weight: 500;
  }

  .tab-button:after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 3px;
    background-color: #3498db;
    transition: width 0.3s ease;
  }

  .tab-button.active {
    color: #3498db;
  }

  .tab-button.active:after {
    width: 100%;
  }

  .tab-button:hover:not(.active) {
    color: #2980b9;
  }

  .content-box {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    overflow-y: visible;
    display: none;
  }

  .content-box.active {
    display: block;
  }

  h1,
  h2,
  h3 {
    color: #2c3e50;
  }

  h1 {
    font-size: 2rem;
    margin-top: 0;
  }

  h2 {
    margin-bottom: 1.3rem;
  }

  p:not(.link) {
    line-height: 1.6;
    margin-bottom: 1.2rem;
  }

  a {
    color: #3498db;
    text-decoration: none;
  }

  a:hover {
    text-decoration: underline;
  }

  ul {
    padding-left: 20px;
    margin-bottom: 1rem;
  }
  li {
    margin-bottom: 0.3rem;
  }

  .content-box > *:last-child {
    margin-bottom: 0;
  }

  .video-container {
    display: flex;
    justify-content: center;
    width: 100%;
    padding-bottom: 25px;
    padding-top: 25px;
  }

  .video-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 560px;
  }

  .video-title {
    margin-bottom: 10px;
    font-size: 1.5rem;
    text-align: center;
    color: #336699;
  }

  /* Add responsive adjustments */
  @media (max-width: 768px) {
    .video-container iframe {
      width: 100%;
      height: auto;
      aspect-ratio: 16/9;
    }
    .tab-navigation {
      flex-direction: row;
      overflow-x: auto;
      justify-content: flex-start;
      padding-bottom: 5px;
    }

    .tab-button {
      padding: 10px 15px;
      font-size: 1rem;
      white-space: nowrap;
    }

    .content-box {
      max-height: 500px;
    }
  }
</style>
