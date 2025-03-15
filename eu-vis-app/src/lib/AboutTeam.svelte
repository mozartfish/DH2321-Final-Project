<main>
  <div class="main-container">
    <div class="title">
      <h4>Meet the Team</h4>
    </div>

    <div class="team-container">
      <div class="team-grid-1">
        <div class="team-member">
          <img src="src/assets/profiles/antonia.png" alt="Antonia" />
          <h3>Antonia</h3>
          <hr />
          <p>Data Processing, Front End, UI/UX, Research</p>
        </div>

        <div class="team-member">
          <img src="src/assets/profiles/fanny.png" alt="Fanny" />
          <h3>Fanny</h3>
          <hr />
          <p>Front End, UI/UX, Testing and Evaluation</p>
        </div>

        <div class="team-member">
          <img src="src/assets/profiles/pranav.png" alt="Pranav" />
          <h3>Pranav</h3>
          <hr />
          <p>Front End, Back End, Research</p>
        </div>
      </div>

      <div class="team-grid-2">
        <div class="team-member">
          <img src="src/assets/profiles/matei.png" alt="Matei" />
          <h3>Matei</h3>
          <hr />
          <p>Data Processing, Front End, Back End, Research</p>
        </div>

        <div class="team-member">
          <img src="src/assets/profiles/safi.png" alt="Safi" />
          <h3>Safi</h3>
          <hr />
          <p>Front End, Back End, Research</p>
        </div>
      </div>
    </div>

    <div class="content-box">
      <h3>Github Repository</h3>
      <a href="https://github.com/mozartfish/DH2321-Final-Project"
        >https://github.com/mozartfish/DH2321-Final-Project</a
      >
    </div>
  </div>
</main>

<style>
  .main-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }

  .title {
    font-size: 30px;
    font-weight: bold;
    background: none;
    border: none;
    position: relative;
    border-bottom: 3px solid black;
    padding-top: 30px;
  }

  .team-container {
    text-align: center;
  }

  .team-grid-1 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    max-width: 600px;
    justify-content: center;
    margin: 0 auto;
  }

  .team-grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    max-width: 400px;
    justify-content: center;
    margin: 0 auto;
    padding: 20px;
  }

  .team-member {
    background: white;
    padding: 20px;
    border-radius: 10px;
    border: 2px solid black;
    box-shadow: 4px 4px 0px black;
    text-align: center;
    width: 180px;
  }

  .team-member img {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 50%;
    border: 2px solid black;
  }

  .team-member h3,
  .team-member p {
    color: black;
  }

  .content-box {
    background: white;
    padding: 20px;
    border-radius: 10px;
    border: 2px solid black;
    box-shadow: 4px 4px 0px black;
    text-align: center;
    width: 400px;
    color: black;
    position: relative;
  }
</style>
