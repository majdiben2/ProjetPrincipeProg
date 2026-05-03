const etat = {
  auteurs: [],
  livres: [],
  lecteurs: [],
  cartes: [],
  emprunts: [],
};

const element = (id) => document.getElementById(id);

function afficherAlerte(message, type = "success") {
  const alerte = element("alert");
  alerte.textContent = message;
  alerte.className = `alert ${type}`;
  window.clearTimeout(afficherAlerte.timer);
  afficherAlerte.timer = window.setTimeout(() => alerte.className = "alert hidden", 4500);
}

async function requeteApi(chemin, options = {}) {
  const reponse = await fetch(chemin, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  const typeContenu = reponse.headers.get("content-type") || "";
  const donnees = typeContenu.includes("application/json") ? await reponse.json() : await reponse.text();

  if (!reponse.ok) {
    const detail = donnees?.detail || donnees?.message || reponse.statusText;
    throw new Error(Array.isArray(detail) ? detail.map(item => item.msg).join(" | ") : detail);
  }
  return donnees;
}

function creerOption(valeur, texte) {
  const option = document.createElement("option");
  option.value = valeur;
  option.textContent = texte;
  return option;
}

function formaterDate(valeur) {
  if (!valeur) return "—";
  return new Date(valeur).toLocaleString("fr-FR");
}

function nomAuteur(id) {
  return etat.auteurs.find(auteur => auteur.id === id)?.name || `Auteur #${id}`;
}

function nomLecteur(id) {
  const lecteur = etat.lecteurs.find(item => item.id === id);
  return lecteur ? `${lecteur.first_name} ${lecteur.last_name}` : `Lecteur #${id}`;
}

function titreLivre(id) {
  return etat.livres.find(livre => livre.id === id)?.title || `Livre #${id}`;
}

function viderFormulaire(formulaireId) {
  element(formulaireId).reset();
  const champCache = element(formulaireId).querySelector('input[type="hidden"]');
  if (champCache) champCache.value = "";
}

async function chargerTout() {
  await Promise.all([chargerAuteurs(), chargerLecteurs()]);
  await Promise.all([chargerLivres(), chargerCartes(), chargerEmprunts()]);
  mettreAJourStatistiques();
}

async function chargerAuteurs() {
  etat.auteurs = await requeteApi("/authors");
  afficherAuteurs();
  remplirSelectAuteurs();
}

async function chargerLivres() {
  etat.livres = await requeteApi("/books");
  afficherLivres();
  remplirSelectLivresEmprunt();
}

async function chargerLecteurs() {
  etat.lecteurs = await requeteApi("/readers");
  afficherLecteurs();
  remplirSelectLecteurs();
}

async function chargerCartes() {
  etat.cartes = await requeteApi("/cards");
  afficherCartes();
}

async function chargerEmprunts() {
  etat.emprunts = await requeteApi("/borrows");
  afficherEmprunts();
}

function mettreAJourStatistiques() {
  element("authorsCount").textContent = etat.auteurs.length;
  element("booksCount").textContent = etat.livres.length;
  element("readersCount").textContent = etat.lecteurs.length;
  element("activeBorrowsCount").textContent = etat.emprunts.filter(emprunt => emprunt.status === "borrowed").length;
}

function afficherAuteurs() {
  element("authorsTable").innerHTML = etat.auteurs.map(auteur => `
    <tr>
      <td>${auteur.id}</td>
      <td>${auteur.name}</td>
      <td>${auteur.nationality || "—"}</td>
      <td>${auteur.birth_year || "—"}</td>
      <td class="actions">
        <button class="button secondary" onclick="modifierAuteur(${auteur.id})">Modifier</button>
        <button class="button danger" onclick="supprimerAuteur(${auteur.id})">Supprimer</button>
      </td>
    </tr>`).join("") || ligneVide(5);
}

function afficherLivres() {
  element("booksTable").innerHTML = etat.livres.map(livre => `
    <tr>
      <td>${livre.id}</td>
      <td>${livre.title}</td>
      <td>${livre.isbn}</td>
      <td>${livre.publication_year || "—"}</td>
      <td>${livre.available_copies}</td>
      <td>${nomAuteur(livre.author_id)}</td>
      <td class="actions">
        <button class="button secondary" onclick="modifierLivre(${livre.id})">Modifier</button>
        <button class="button danger" onclick="supprimerLivre(${livre.id})">Supprimer</button>
      </td>
    </tr>`).join("") || ligneVide(7);
}

function afficherLecteurs() {
  element("readersTable").innerHTML = etat.lecteurs.map(lecteur => `
    <tr>
      <td>${lecteur.id}</td>
      <td>${lecteur.first_name}</td>
      <td>${lecteur.last_name}</td>
      <td>${lecteur.email}</td>
      <td class="actions">
        <button class="button secondary" onclick="modifierLecteur(${lecteur.id})">Modifier</button>
        <button class="button danger" onclick="supprimerLecteur(${lecteur.id})">Supprimer</button>
      </td>
    </tr>`).join("") || ligneVide(5);
}

function afficherCartes() {
  element("cardsTable").innerHTML = etat.cartes.map(carte => `
    <tr>
      <td>${carte.id}</td>
      <td>${carte.card_number}</td>
      <td>${nomLecteur(carte.reader_id)}</td>
      <td>${formaterDate(carte.issued_at)}</td>
      <td class="actions">
        <button class="button secondary" onclick="modifierCarte(${carte.id})">Modifier</button>
        <button class="button danger" onclick="supprimerCarte(${carte.id})">Supprimer</button>
      </td>
    </tr>`).join("") || ligneVide(5);
}

function afficherEmprunts() {
  element("borrowsTable").innerHTML = etat.emprunts.map(emprunt => `
    <tr>
      <td>${emprunt.id}</td>
      <td>${nomLecteur(emprunt.reader_id)}</td>
      <td>${titreLivre(emprunt.book_id)}</td>
      <td>${formaterDate(emprunt.borrow_date)}</td>
      <td>${formaterDate(emprunt.return_date)}</td>
      <td><span class="badge ${emprunt.status}">${emprunt.status}</span></td>
      <td class="actions">
        ${emprunt.status === "borrowed" ? `<button class="button success" onclick="retournerEmprunt(${emprunt.id})">Retourner</button>` : ""}
        <button class="button danger" onclick="supprimerEmprunt(${emprunt.id})">Supprimer</button>
      </td>
    </tr>`).join("") || ligneVide(7);
}

function ligneVide(nombreColonnes) {
  return `<tr><td colspan="${nombreColonnes}">Aucune donnée pour le moment.</td></tr>`;
}

function remplirSelectAuteurs() {
  const select = element("bookAuthorId");
  select.innerHTML = "";
  etat.auteurs.forEach(auteur => select.append(creerOption(auteur.id, `${auteur.name} (#${auteur.id})`)));
}

function remplirSelectLecteurs() {
  ["cardReaderId", "borrowReaderId"].forEach(id => {
    const select = element(id);
    select.innerHTML = "";
    etat.lecteurs.forEach(lecteur => select.append(creerOption(lecteur.id, `${lecteur.first_name} ${lecteur.last_name} (#${lecteur.id})`)));
  });
}

function remplirSelectLivresEmprunt() {
  const select = element("borrowBookId");
  select.innerHTML = "";
  etat.livres.forEach(livre => {
    const texte = `${livre.title} (#${livre.id}) — ${livre.available_copies} copie(s)`;
    select.append(creerOption(livre.id, texte));
  });
}

window.modifierAuteur = (id) => {
  const auteur = etat.auteurs.find(item => item.id === id);
  element("authorId").value = auteur.id;
  element("authorName").value = auteur.name;
  element("authorNationality").value = auteur.nationality || "";
  element("authorBirthYear").value = auteur.birth_year || "";
};

window.modifierLivre = (id) => {
  const livre = etat.livres.find(item => item.id === id);
  element("bookId").value = livre.id;
  element("bookTitle").value = livre.title;
  element("bookIsbn").value = livre.isbn;
  element("bookPublicationYear").value = livre.publication_year || "";
  element("bookAvailableCopies").value = livre.available_copies;
  element("bookAuthorId").value = livre.author_id;
};

window.modifierLecteur = (id) => {
  const lecteur = etat.lecteurs.find(item => item.id === id);
  element("readerId").value = lecteur.id;
  element("readerFirstName").value = lecteur.first_name;
  element("readerLastName").value = lecteur.last_name;
  element("readerEmail").value = lecteur.email;
};

window.modifierCarte = (id) => {
  const carte = etat.cartes.find(item => item.id === id);
  element("cardId").value = carte.id;
  element("cardNumber").value = carte.card_number;
  element("cardReaderId").value = carte.reader_id;
};

window.supprimerAuteur = async (id) => {
  if (!confirm("Supprimer cet auteur ? Les livres associés peuvent aussi être supprimés.")) return;
  await gererAction(() => requeteApi(`/authors/${id}`, { method: "DELETE" }), "Auteur supprimé");
};

window.supprimerLivre = async (id) => {
  if (!confirm("Supprimer ce livre ?")) return;
  await gererAction(() => requeteApi(`/books/${id}`, { method: "DELETE" }), "Livre supprimé");
};

window.supprimerLecteur = async (id) => {
  if (!confirm("Supprimer ce lecteur ? Sa carte et ses emprunts seront aussi supprimés.")) return;
  await gererAction(() => requeteApi(`/readers/${id}`, { method: "DELETE" }), "Lecteur supprimé");
};

window.supprimerCarte = async (id) => {
  if (!confirm("Supprimer cette carte ?")) return;
  await gererAction(() => requeteApi(`/cards/${id}`, { method: "DELETE" }), "Carte supprimée");
};

window.supprimerEmprunt = async (id) => {
  if (!confirm("Supprimer cet emprunt ?")) return;
  await gererAction(() => requeteApi(`/borrows/${id}`, { method: "DELETE" }), "Emprunt supprimé");
};

window.retournerEmprunt = async (id) => {
  await gererAction(() => requeteApi(`/borrows/${id}/return`, { method: "PATCH" }), "Livre retourné");
};

async function gererAction(action, messageSucces) {
  try {
    await action();
    afficherAlerte(messageSucces, "success");
    await chargerTout();
  } catch (erreur) {
    afficherAlerte(erreur.message, "error");
  }
}

element("authorForm").addEventListener("submit", async (evenement) => {
  evenement.preventDefault();
  const id = element("authorId").value;
  const donnees = {
    name: element("authorName").value,
    nationality: element("authorNationality").value || null,
    birth_year: element("authorBirthYear").value ? Number(element("authorBirthYear").value) : null,
  };
  await gererAction(
    () => requeteApi(id ? `/authors/${id}` : "/authors", { method: id ? "PUT" : "POST", body: JSON.stringify(donnees) }),
    id ? "Auteur modifié" : "Auteur créé"
  );
  viderFormulaire("authorForm");
});

element("bookForm").addEventListener("submit", async (evenement) => {
  evenement.preventDefault();
  const id = element("bookId").value;
  const donnees = {
    title: element("bookTitle").value,
    isbn: element("bookIsbn").value,
    publication_year: element("bookPublicationYear").value ? Number(element("bookPublicationYear").value) : null,
    available_copies: Number(element("bookAvailableCopies").value || 0),
    author_id: Number(element("bookAuthorId").value),
  };
  await gererAction(
    () => requeteApi(id ? `/books/${id}` : "/books", { method: id ? "PUT" : "POST", body: JSON.stringify(donnees) }),
    id ? "Livre modifié" : "Livre créé"
  );
  viderFormulaire("bookForm");
});

element("readerForm").addEventListener("submit", async (evenement) => {
  evenement.preventDefault();
  const id = element("readerId").value;
  const donnees = {
    first_name: element("readerFirstName").value,
    last_name: element("readerLastName").value,
    email: element("readerEmail").value,
  };
  await gererAction(
    () => requeteApi(id ? `/readers/${id}` : "/readers", { method: id ? "PUT" : "POST", body: JSON.stringify(donnees) }),
    id ? "Lecteur modifié" : "Lecteur créé"
  );
  viderFormulaire("readerForm");
});

element("cardForm").addEventListener("submit", async (evenement) => {
  evenement.preventDefault();
  const id = element("cardId").value;
  const donnees = {
    card_number: element("cardNumber").value,
    reader_id: Number(element("cardReaderId").value),
  };
  await gererAction(
    () => requeteApi(id ? `/cards/${id}` : "/cards", { method: id ? "PUT" : "POST", body: JSON.stringify(donnees) }),
    id ? "Carte modifiée" : "Carte créée"
  );
  viderFormulaire("cardForm");
});

element("borrowForm").addEventListener("submit", async (evenement) => {
  evenement.preventDefault();
  const donnees = {
    reader_id: Number(element("borrowReaderId").value),
    book_id: Number(element("borrowBookId").value),
  };
  await gererAction(
    () => requeteApi("/borrows", { method: "POST", body: JSON.stringify(donnees) }),
    "Emprunt créé"
  );
  viderFormulaire("borrowForm");
});

element("resetAuthorForm").addEventListener("click", () => viderFormulaire("authorForm"));
element("resetBookForm").addEventListener("click", () => viderFormulaire("bookForm"));
element("resetReaderForm").addEventListener("click", () => viderFormulaire("readerForm"));
element("resetCardForm").addEventListener("click", () => viderFormulaire("cardForm"));
element("refreshAllBtn").addEventListener("click", () => gererAction(chargerTout, "Données actualisées"));

document.querySelectorAll("[data-refresh]").forEach(bouton => {
  bouton.addEventListener("click", () => gererAction(chargerTout, "Données actualisées"));
});

document.querySelectorAll(".tab").forEach(onglet => {
  onglet.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(item => item.classList.remove("active"));
    document.querySelectorAll(".panel").forEach(panneau => panneau.classList.remove("active"));
    onglet.classList.add("active");
    element(onglet.dataset.tab).classList.add("active");
  });
});

chargerTout().catch(erreur => afficherAlerte(erreur.message, "error"));
