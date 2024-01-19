const form = document.querySelector("form"),
      fileInput = document.querySelector(".file-input"),
      loadingRing = document.querySelector(".lds-ring"),
      wrapper = document.querySelector(".wrapper");
      
form.addEventListener("click", () => fileInput.click());

fileInput.onchange = ({ target }) => {
  let file = target.files[0];
  if (file) {
    if (file.type === "application/pdf") {
      wrapper.style.display = "none";
      loadingRing.style.display = "inline-block";
    } else {
      console.log("O arquivo não é um PDF");
    }
  }
}