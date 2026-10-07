import re,html
esc=html.escape
src=open('index.html').read()

# ---------- reuse the site header / mobile menu / footer, re-pointing anchors to index.html ----------
def fix(s): return re.sub(r'href="#(?!")([^"]+)"',r'href="index.html#\1"',s)
header=re.search(r'<header class="nav">.*?</header>',src,re.S).group(0)
header=fix(header).replace('href="index.html#"','href="index.html"')
footer=fix(re.search(r'<footer class="foot on-dark">.*?</footer>',src,re.S).group(0)).replace('href="index.html#"','href="index.html"')
footer=footer.replace('href="design-system.html"','href="design-system.html"')
header=header.replace('<a class="logo" href="index.html#"','<a class="logo" href="index.html"')

K='https://www.kiwili.com'
topics=[
 ("Premiers pas",[("Démarrer dans Kiwili",K+"/fr/Blog/post/bien-demarrer-dans-kiwili/"),("Gestion des droits d'accès",None)]),
 ("Clients et équipe",[("Clients et fournisseurs",K+"/fr/aide-clients-fournisseurs-erp-avec-kiwili/"),("Gérer son temps",K+"/aide-gestion-temps-avec-kiwili/")]),
 ("Projets",[("Gérer un projet",K+"/Blog/post/4-gerer-un-projet-avec-kiwili/"),("Créer et gérer une tâche",K+"/Blog/post/creer-gerer-une-tache-avec-kiwili/")]),
 ("Ventes et achats",[("Émettre un devis",K+"/Blog/post/3-emettre-un-devis-avec-kiwili/"),("Émettre une facture",K+"/Blog/post/5-emettre-une-facture-avec-kiwili/"),("Gérer ses dépenses",K+"/Blog/post/gerer-ses-depenses-avec-kiwili/"),("Bons de commande en ligne",K+"/Blog/post/la-gestion-des-bons-de-commande-en-ligne/")]),
 ("Finances",[("Prévoir la trésorerie",K+"/Blog/post/tresorerie-prevoir-solde-compte-bancaire-entreprise/"),("Option COMPTABILITÉ+",K+"/aide-gestion-option-comptabilite-kiwili/")]),
 ("Besoin d'aide ?",[("Contacter le support",K+"/Blog/post/contacter-le-support-de-kiwili/")]),
]
side=''
for g,items in topics:
    cur=any(u is None for _,u in items)
    lis=''.join((f'<li><a class="cur" href="#top" aria-current="page">{esc(t)}</a></li>' if u is None else f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)}</a></li>') for t,u in items)
    side+=f'<details class="tg"{" open" if cur else ""}><summary>{esc(g)}<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></summary><ul>{lis}</ul></details>'

def ul(items,cls=''): return f'<ul class="{cls}">'+''.join(f'<li>{i}</li>' for i in items)+'</ul>' if items else ''
def lst(can=None,cannot=None):
    o=''
    if can: o+=f'<div class="cc ok"><h4>{can[0]}</h4>{ul(can[1])}</div>'
    if cannot: o+=f'<div class="cc no"><h4>{cannot[0]}</h4>{ul(cannot[1])}</div>'
    return f'<div class="ccgrid">{o}</div>' if o else ''
def fig(name,alt,cap=''):
    return f'<figure class="shot-fig"><img src="assets/tuto/{name}.webp" alt="{esc(alt)}" loading="lazy" decoding="async"><figcaption>{esc(cap)}</figcaption></figure>' if cap else f'<figure class="shot-fig"><img src="assets/tuto/{name}.webp" alt="{esc(alt)}" loading="lazy" decoding="async"></figure>'
def compare(a,b,cap):
    return f'''<div class="compare" data-compare><div class="cmp-tabs" role="tablist" aria-label="Comparer deux vues"><button type="button" role="tab" class="on" aria-selected="true" data-i="0">{esc(a[0])}</button><button type="button" role="tab" aria-selected="false" data-i="1">{esc(b[0])}</button></div><div class="cmp-stage"><img class="on" src="assets/tuto/{a[1]}.webp" alt="{esc(a[2])}" loading="lazy" decoding="async"><img src="assets/tuto/{b[1]}.webp" alt="{esc(b[2])}" loading="lazy" decoding="async"></div><p class="cmp-cap">{esc(cap)}</p></div>'''
def note(kind,text): return f'<p class="callout {kind}">{text}</p>'
def table(head,rows):
    return '<div class="tw"><table class="mini"><thead><tr>'+''.join(f'<th>{h}</th>' for h in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'</tbody></table></div>'
OK='<span class="pill ok">Autorisé</span>'; NO='<span class="pill no">Non autorisé</span>'

groups=[]
# ---- Administration
adm=[
 dict(id='administrateur',t='Administrateur',tag='Accès total',body=
  '<p>Le système requiert au moins un administrateur. Celui-ci a un accès total aux fonctionnalités et aux données financières du compte Kiwili. Il gère tous les droits d’accès des autres utilisateurs.</p>'
  +table(['Module','Ce que l’administrateur peut faire'],[
   ['Configuration','Gérer les utilisateurs, le profil d’entreprise, les informations de paiement, le forfait Kiwili, l’historique des prélèvements, les modèles globaux de documents, la gestion des messages et le suivi de projet.'],
   ['Indicateurs','Voir le graphique global et le tableau des données financières.'],
   ['Clients et fournisseurs','Accéder à toutes les informations. Une personne qui n’est pas administrateur ne voit pas, dans la fiche client ou fournisseur, les projets sur lesquels elle ne travaille pas.'],
   ['Projets','Voir le graphique de charge de travail, les salaires et les trois types de marges, dans tous les projets, qu’il en soit membre ou non. Dans l’onglet temps, accéder à toutes les données de salaires et financières.'],
   ['Rapports','Accéder aux rapports d’activité et de courriels, à toutes les informations de salaire et de coût horaire, ainsi qu’à la recherche des entrées de temps.']])
  +note('info','Un utilisateur qui n’est pas administrateur d’un projet ne voit pas certaines informations, comme la charge de travail, le tableau des tâches ou les tâches des autres utilisateurs.')),
 dict(id='configuration',t='Configuration',tag='Partiel',body=
  '<p>Avec l’accès configuration, l’utilisateur peut paramétrer et modifier de nombreux éléments, bien que certains restent réservés à l’administrateur. Voici le détail des accès pour chaque encart de la configuration.</p>'
  +table(['Encart','Accès'],[['Abonnement',NO],['Présentation','Uniquement « champs personnalisés (clients et fournisseurs) »'],['Achats et ventes','Accès à tout'],['Comptabilité','Modes de paiement, charte comptable et taxes'],['Extranet',NO]])),
 dict(id='rapports',t='Rapports',tag='Données sensibles',body=
  '<p>Kiwili génère automatiquement de nombreux rapports clairs et complets qui permettent d’extraire des statistiques et des bilans utiles au développement des affaires. Vous pouvez, par exemple, obtenir des rapports précis sur vos impôts et taxes, un graphique de vos dépenses et revenus, ou un graphique des heures travaillées par client. Kiwili propose plus d’une soixantaine de rapports.</p>'
  +note('warn','Ce droit donne accès à de nombreuses informations sensibles. Soyez vigilant et ne l’accordez pas à n’importe qui.')),
 dict(id='api',t='API',tag='Intégrations',body=
  '<p>Pour autoriser certains utilisateurs à connecter leur compte Kiwili à d’autres applications, cochez la case API. Ils pourront alors activer l’API dans leur profil et générer un jeton.</p><p><a href="https://api.kiwili.com/api/openapi/" target="_blank" rel="noopener">Consulter la documentation de l’API</a></p>'),
]
groups.append(('administration','Administration et configuration','blue',adm))
# ---- Temps
groups.append(('temps','Temps','green',[
 dict(id='feuilledetemps',t='Feuille de temps',tag='',body='<p>Cet accès permet à l’utilisateur de gérer son temps. Lorsque « feuille de temps » est coché, il a accès au module temps.</p>'+fig('feuille-de-temps','Onglet temps avec l’accès feuille de temps','L’onglet Temps pour un utilisateur avec l’accès feuille de temps.')+lst(('Dans l’onglet temps, il peut',['entrer le détail de ses heures ;','démarrer plusieurs compteurs (chronomètres) en même temps ;','ajouter du temps depuis une tâche ;','convertir la durée travaillée en entrée de temps.']),('Il ne peut pas',['voir le temps des autres utilisateurs.']))),
 dict(id='feuilledetempsdelequipe',t='Feuille de temps de l’équipe',tag='Implique : feuille de temps',body='<p>Cet accès, qui implique « feuille de temps », donne accès au module temps de toute l’équipe. L’utilisateur peut voir, ajouter et modifier du temps et des tâches pour l’ensemble des utilisateurs.</p><p>Il peut aussi fermer la feuille de temps de l’équipe, c’est-à-dire valider le temps de chaque utilisateur pour qu’il ne soit plus modifiable jusqu’à la date de fermeture. Cela évite les erreurs une fois le temps validé.</p>'),
]))
# ---- Clients
groups.append(('clients','Clients et fournisseurs','orange',[
 dict(id='clientsetfournisseurs',t='Clients et fournisseurs',tag='',body='<p>Avec cet accès, l’utilisateur peut utiliser les modules clients et fournisseurs. Il peut voir, créer et modifier les clients et fournisseurs de l’entreprise. Les données financières (devis, factures, état de compte, soldes) lui sont accessibles selon les autres droits accordés.</p><p>Comparez l’onglet client ou fournisseur d’un utilisateur (accès général, contact, tâches, suivi, espace client) avec celui de l’administrateur, qui a l’accès complet.</p>'+compare(('Utilisateur','clients-restreint','Onglet client vu par un utilisateur'),('Administrateur','admin-complet','Onglet client vu par l’administrateur'),'Fiche client : vue de l’utilisateur et vue de l’administrateur.')),
 dict(id='arclientsetfournisseurs',t='Accès restreint aux clients et fournisseurs',tag='',body='<p>L’utilisateur ne peut accéder qu’aux clients et fournisseurs dont il est administrateur.</p>'),
]))
# ---- Projets
groups.append(('projets','Projets et tâches','blue',[
 dict(id='projets',t='Projets',tag='',body='<p>Ce droit permet à un utilisateur d’accéder aux projets dont il est administrateur ou usager. Il peut voir, créer et modifier ses projets ainsi que leurs étapes et leurs tâches.</p>'+note('info','Il n’a accès à aucune donnée financière. Seuls les administrateurs du compte Kiwili y ont accès en totalité.')),
 dict(id='projetsrestreints',t='Projets restreints',tag='',body='<p>Cet accès ne permet pas à l’utilisateur de créer un projet.</p>'+lst(('Il peut',['accéder à la liste de ses projets ;','voir les tâches, les heures et les suivis de ses projets.']),('Masqué pour lui',['les données financières : général, devis, factures et bons de commande.']))+compare(('Accès restreint','projet-restreint','Projet vu avec l’accès projets restreints'),('Administrateur','admin-complet','Projet vu par l’administrateur du compte'),'Le même projet, vu avec l’accès restreint et par l’administrateur du compte Kiwili.')),
 dict(id='gestionnairedeprojet',t='Gestionnaire de projet',tag='Option : avec salaire',body='<p>L’utilisateur peut modifier les projets dont il est administrateur et voir plus d’informations financières sur ces projets, sans pouvoir déterminer le salaire d’un employé (sauf s’il a aussi le droit « salaire »).</p><p>Le statut de gestionnaire de projet donne accès aux modules suivants, mais seulement pour les projets dont l’utilisateur est administrateur :</p>'+ul(['Projets (il ne peut pas créer de projet si l’accès projets n’est pas activé) ;','Tâches (non touché par ce rôle) ;','Temps (gestion du temps seulement, si l’accès temps n’est pas activé) ;','Devis, factures et dépenses de ses projets.'])+'<h4>Avec salaire</h4><p>Le droit « avec salaire », que vous pouvez ajouter à « gestionnaire de projet », donne accès aux données liées au salaire : la charge salariale des projets, la charge de travail allouée au projet et le rapport avec les heures.</p>'),
 dict(id='tachesrestreintes',t='Tâches restreintes',tag='',body='<p>Le <a href="https://www.kiwili.com/Blog/post/creer-gerer-une-tache-avec-kiwili/" target="_blank" rel="noopener">module tâches</a> de Kiwili permet de planifier, structurer et suivre les tâches de façon intuitive. Avec « tâches restreintes », l’utilisateur n’a accès qu’aux tâches qui lui sont assignées ou qu’il a créées. Il peut essentiellement commenter une tâche, renseigner son statut et entrer son temps.</p>'+lst(('Il peut aussi',['créer et planifier ses tâches (sans les lier aux services ni aux étapes d’un projet) ;','voir toutes les tâches d’un projet auquel il est assigné ;','indiquer une priorité, une échéance et un nombre d’heures prévues par tâche ;','entrer des messages de suivi ;','ajouter des documents et des pièces jointes ;','voir l’historique des modifications ;','importer et exporter des tâches.']),('S’il est administrateur d’une tâche, il peut en plus',['créer et assigner des tâches à d’autres membres de l’équipe, s’ils sont sur le même projet ;','modifier ses tâches ou celles qu’il a assignées à d’autres utilisateurs.']))),
 dict(id='sprints',t='Sprints',tag='Certains forfaits',body='<p>Avec ce droit, l’utilisateur accède aux fonctions « Sprints » de l’onglet tâches, pour les sprints auxquels il participe :</p>'+ul(['la date de début et de fin ;','le statut du sprint ;','l’administrateur du sprint ;','la description ;','les ressources allouées et leurs informations ;','toutes les tâches incluses dans le sprint.'])+'<p>Si « tâches restreintes » est coché, il ne voit que les tâches qui lui sont assignées, et non toutes celles du sprint.</p>'+note('info','Fonctionnalité disponible uniquement dans certains forfaits.')),
 dict(id='admindesprints',t='Administrateur de sprints',tag='Certains forfaits',body='<p>En plus de consulter les sprints, ce droit permet d’en modifier les informations, de créer de nouveaux sprints et de les archiver.</p>'+note('info','Fonctionnalité disponible uniquement dans certains forfaits.')),
]))
# ---- Ventes
groups.append(('ventes','Devis et factures','green',[
 dict(id='devis',t='Devis',tag='',body='<p>Ce droit permet de créer et d’émettre des devis professionnels en intégrant facilement toutes les informations indispensables. Pour en savoir plus, lisez notre <a href="https://www.kiwili.com/Blog/post/3-emettre-un-devis-avec-kiwili/" target="_blank" rel="noopener">article sur les devis</a>.</p><p>L’utilisateur a accès au module devis, mais certaines fonctions lui sont inaccessibles sans les autres droits :</p>'+lst(None,('Il ne peut pas',['modifier le modèle global du devis sans « configuration » ;','voir et associer un projet à un devis s’il n’est pas administrateur ou usager de ce projet et n’a pas « projets » ;','convertir un devis en projet ou en facture sans « projets » ou « factures » ;','ajouter un prospect ou accéder à la fiche client sans « clients et fournisseurs ».']))),
 dict(id='factures',t='Factures',tag='',body='<p>Ce droit permet de créer et d’émettre rapidement des factures professionnelles. Pour en savoir plus, lisez notre <a href="https://www.kiwili.com/Blog/post/5-emettre-une-facture-avec-kiwili/" target="_blank" rel="noopener">article sur les factures</a>.</p><p>L’utilisateur a accès au module factures, mais certaines fonctions lui sont inaccessibles sans les autres droits :</p>'+lst(None,('Il ne peut pas',['modifier le modèle global de la facture sans « configuration » ;','voir et associer un projet à une facture s’il n’est pas administrateur ou usager de ce projet et n’a pas « projets » ;','importer une dépense ou du temps sans « dépenses » ou « temps » ;','ajouter un prospect ou accéder à la fiche client sans « clients » ;','accéder aux devis et convertir un devis en facture sans « devis » ;','accéder au module de paiement sans « paiements ».']))),
]))
# ---- Dépenses et achats
groups.append(('depenses','Dépenses et achats','orange',[
 dict(id='depensespersonnelles',t='Dépenses personnelles',tag='',body='<p>Grâce à cet accès, l’utilisateur saisit et gère simplement les dépenses qu’il a effectuées. Consultez notre article sur la <a href="https://www.kiwili.com/Blog/post/gerer-ses-depenses-avec-kiwili/" target="_blank" rel="noopener">gestion des dépenses</a>.</p>'+lst(('Il peut',['ajouter des dépenses régulières, groupées et récurrentes, uniquement pour lui ;','joindre des reçus ou d’autres documents à ses dépenses ;','renseigner la date, le poste (avec ou sans code comptable), le numéro de facture fournisseur, la description, le prix (hors taxes ou taxes incluses : les taxes se calculent automatiquement dans les deux sens) et la quantité ;','exporter ses dépenses au format PDF ou XML.']),('Il ne peut pas',['lier ses dépenses à des clients, fournisseurs ou projets sans « clients/fournisseurs » ou « projets » ;','accéder au module de paiement sans « paiements » ;','convertir une dépense en facture sans « factures » ;','modifier le statut d’une dépense sans « dépenses de l’équipe » ;','annuler une dépense, même au statut de brouillon, sans « dépenses de l’équipe ».']))),
 dict(id='depensesdelequipe',t='Dépenses de l’équipe',tag='Inclut : dépenses personnelles',body='<p>Cet accès inclut les dépenses personnelles. L’utilisateur peut donc ajouter des dépenses en son nom et au nom d’autres utilisateurs.</p>'+lst(('Une fois la dépense créée, il peut',['indiquer qui a encouru la dépense ;','choisir le fournisseur lié à la dépense ;','sélectionner le projet lié, uniquement s’il en est usager ;','faire passer le statut de brouillon à « à payer » ;','annuler ou supprimer une dépense au statut de brouillon.']),None)+note('info','Il ne peut pas saisir le statut « payé », convertir des dépenses en factures ni entrer de paiements sans les droits nécessaires (paiements et factures).')),
 dict(id='bondecommande',t='Bon de commande',tag='',body='<p>Cet accès permet de créer et de gérer des bons de commande fournisseurs. Pour en apprendre plus, lisez notre <a href="https://www.kiwili.com/Blog/post/la-gestion-des-bons-de-commande-en-ligne/" target="_blank" rel="noopener">article sur les bons de commande</a>.</p>'+lst(('Il peut',['ajouter un bon de commande ;','sélectionner le fournisseur et le contact fournisseur ;','sélectionner un projet, uniquement s’il en est usager ;','définir les dates de commande, d’expédition et de livraison ;','transmettre le bon de commande au fournisseur ;','l’exporter en bon de livraison au format PDF ;','modifier son statut (brouillon, transmis, expédié, partiellement livré, livré, annulé).']),('Il n’a pas accès à',['la modification de l’acheteur du bon de commande ;','la gestion des commandes ;','la configuration du bon de commande (modèle global) sans « configuration » ;','la conversion du bon de commande en dépense sans « dépenses ».']))),
 dict(id='bondecommandedelequipe',t='Bon de commande de l’équipe',tag='Inclut : bon de commande',body='<p>Cet accès est similaire à « bon de commande ». Il offre les mêmes fonctionnalités et permet en plus de désigner d’autres utilisateurs comme acheteurs et de gérer les commandes.</p>'),
]))
# ---- Finances
groups.append(('finances','Finances et comptabilité','blue',[
 dict(id='paiements',t='Paiements',tag='Se combine avec factures et dépenses',body='<p>Ce droit a été créé pour permettre à un utilisateur de saisir des paiements sur une facture ou des dépenses. Il doit être combiné avec les droits « factures » et « dépenses de l’équipe » pour permettre de saisir des paiements.</p>'),
 dict(id='budget',t='Budget',tag='Trésorerie',body='<p>Cet accès permet à l’utilisateur d’ouvrir le module trésorerie et d’avoir une vue prévisionnelle de la trésorerie sur 3 à 12 mois. Voir aussi l’<a href="https://www.kiwili.com/Blog/post/tresorerie-prevoir-solde-compte-bancaire-entreprise/" target="_blank" rel="noopener">article sur la trésorerie</a>.</p>'+lst(('Il peut',['entrer des revenus et des dépenses prévisionnels ;','saisir le solde actuel du compte bancaire, s’il possède cette information ;','voir le tableau prévisionnel de l’entreprise.']),None)),
 dict(id='comptesbancaires',t='Comptes bancaires',tag='Avec : configuration',body='<p>Cet accès permet à un autre utilisateur de configurer vos comptes bancaires dans Kiwili. Il peut les voir, les modifier ou en ajouter de nouveaux. Il fonctionne uniquement si l’utilisateur a aussi l’accès « configuration ».</p>'+note('info','Pour accéder à la conciliation bancaire, le droit « comptes bancaires » doit être coché.')),
 dict(id='comptabilite',t='Comptabilité',tag='Option COMPTABILITÉ+',body='<p>Ce droit donne accès à l’<a href="https://www.kiwili.com/aide-gestion-option-comptabilite-kiwili/" target="_blank" rel="noopener">option COMPTABILITÉ+</a>. Voici ce que l’utilisateur peut faire lorsque vous cochez cet accès.</p>'
  +'<h4>Dans Banque</h4>'+table(['Fonction','Accès'],[['Conciliation bancaire',NO+' (il faut aussi le droit « comptes bancaires »)'],['Rapport de conciliation bancaire',OK],['Impression de chèque','Création d’un chèque à partir d’une entrée de journal. Pas de nouveau chèque à un fournisseur sans le droit « paiements ».']])
  +'<h4>Dans COMPTABILITÉ+</h4>'+table(['Fonction','Accès'],[['Entrées manuelles du journal général',OK],['Journal général',OK],['Grand livre','Rapport de l’ensemble des comptes de l’entreprise, mais pas par projet'],['Balance de vérification',OK],['États des résultats','Rapport général, mais pas par projet'],['Bilan',OK],['Solde d’ouverture',OK],['Fermeture de l’année',OK]])
  +'<h4>Dans Rapports standards</h4>'+table(['Rapport','Accès'],[['Codes comptables',NO],['Comptes à recevoir',NO],['État de compte',NO],['Comptes à payer',NO],['Paiements',NO],['Taxes',NO],['Registre de détention des sommes',NO],['Fichier des écritures comptables',OK]])
  +'<h4>Dans Configuration</h4>'+table(['Fonction','Accès'],[['Assistant de configuration COMPTABILITÉ+','Uniquement la configuration des taxes et la définition des comptes'],['Configuration du modèle de chèque',OK],['Début d’exercice financier',NO],['Comptes bancaires pour paiement en ligne',OK]])),
]))

colors={'blue':'--c-blue','green':'--c-green','orange':'--c-orange'}
icons={'administration':'<path d="M12 3l8 3v6c0 4.5-3.2 8-8 9-4.8-1-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>','temps':'<circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 2h6"/>','clients':'<circle cx="9" cy="8" r="3.2"/><path d="M3.5 20c.7-3.6 3-5.3 5.5-5.3s4.8 1.7 5.5 5.3M16 11a3 3 0 1 0 0-6M17.5 14.9c2 .6 3.3 2.2 3.8 5.1"/>','projets':'<path d="M4 6h10M4 12h16M4 18h8"/>','ventes':'<path d="M7 3h8l4 4v14H7z"/><path d="M15 3v4h4M10 12h6M10 16h4"/>','depenses':'<path d="M6 4h12v17H6z"/><path d="M9 4v3h6V4M9 12l2 2 4-4"/>','finances':'<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h2m3 0h3M8 16h2m3 0h3"/>'}
rights=''; chips='<button class="gchip on" type="button" data-g="all">Tous</button>'; total=0
for gid,gt,col,items in groups:
    chips+=f'<button class="gchip" type="button" data-g="{gid}">{esc(gt)}</button>'
    rs=''
    for r in items:
        total+=1
        tag=f'<span class="rtag">{esc(r["tag"])}</span>' if r['tag'] else ''
        rs+=f'<details class="right" id="{r["id"]}" data-s="{esc((r["t"]+" "+r["tag"]+" "+re.sub("<[^>]+>"," ",r["body"])).lower())}"><summary><span class="rname">{esc(r["t"])}</span>{tag}<svg class="rchev" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg></summary><div class="rbody">{r["body"]}</div></details>'
    rights+=f'<section class="rgroup c-{col}" data-g="{gid}" aria-labelledby="h-{gid}"><h3 id="h-{gid}"><span class="gico"><svg viewBox="0 0 24 24" aria-hidden="true">{icons[gid]}</svg></span>{esc(gt)}<small>{len(items)}</small></h3>{rs}</section>'

more=[("Gérer son temps",K+"/aide-gestion-temps-avec-kiwili/"),("Gérer un projet",K+"/Blog/post/4-gerer-un-projet-avec-kiwili/"),("Émettre un devis",K+"/Blog/post/3-emettre-un-devis-avec-kiwili/"),("Émettre une facture",K+"/Blog/post/5-emettre-une-facture-avec-kiwili/"),("Gérer ses dépenses",K+"/Blog/post/gerer-ses-depenses-avec-kiwili/"),("Option COMPTABILITÉ+",K+"/aide-gestion-option-comptabilite-kiwili/")]
morehtml=''.join(f'<a class="more-card" href="{u}" target="_blank" rel="noopener"><span>{esc(t)}</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>' for t,u in more)

page=f'''<!doctype html>
<html lang="fr-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gestion des droits d'accès | Centre d'aide Kiwili</title>
<meta name="description" content="Les droits d'accès encadrent ce que chaque utilisateur peut voir et faire dans votre compte Kiwili. Voici le détail de chacun.">
<meta name="theme-color" content="#070b14">
<link rel="icon" href="assets/logo-mark.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Inter:wght@400..600&family=Caveat:wght@600&display=swap">
<link rel="stylesheet" href="css/tokens.css">
<link rel="stylesheet" href="css/components.css">
<link rel="stylesheet" href="css/home.css">
<link rel="stylesheet" href="css/tutorial.css">
</head>
<body>
<a class="skip" href="#main">Aller au contenu</a>
<div class="read-progress" aria-hidden="true"><i id="read-fill"></i></div>
{header}
<div class="help-bar"><div class="container help-inner">
  <a class="help-title" href="{K}/aide/" target="_blank" rel="noopener">Centre d'aide</a>
  <nav class="help-links" aria-label="Centre d'aide"><a href="{K}/fr/Blog/post/bien-demarrer-dans-kiwili/" target="_blank" rel="noopener">Démarrer</a><a href="{K}/fr/faq-kiwili/" target="_blank" rel="noopener">FAQ</a><a href="{K}/fr/assistance/" target="_blank" rel="noopener">Assistance</a><a href="{K}/fr/formations-en-ligne-logiciel-gestion-entreprise/" target="_blank" rel="noopener">Formations</a></nav>
  <form class="help-search" role="search" id="help-search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg><label class="sr" for="q-top">Rechercher un droit d'accès</label><input id="q-top" type="search" placeholder="Rechercher un droit d'accès" autocomplete="off"></form>
  <a class="btn btn-accent btn-sm" href="https://signup.kiwili.com/signup/?lng=fr" target="_blank" rel="noopener">Essai gratuit</a>
</div></div>

<div class="container tuto" id="top">
  <aside class="tuto-side" aria-label="Sujets du centre d'aide">
    <details class="side-wrap" id="side-wrap" open><summary class="side-sum">Sujets</summary><div class="side-body"><p class="side-h">Sujets</p>{side}</div></details>
  </aside>

  <main id="main" class="tuto-main">
   <article>
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="{K}/aide/" target="_blank" rel="noopener">Centre d'aide</a><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg><span>Premiers pas</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg><span aria-current="page">Gestion des droits d'accès</span></nav>
    <header class="art-head">
      <span class="eyebrow">Tutoriel</span>
      <h1>Gestion des droits d'accès</h1>
      <p class="lede">Les droits d'accès offrent un meilleur encadrement des accès destinés aux employés ou aux collaborateurs qui utilisent votre compte Kiwili. Voici le détail de chacun.</p>
    </header>

    <nav class="toc" aria-labelledby="toc-h"><p class="toc-h" id="toc-h">Dans cet article</p><ol>
      <li><a href="#definition"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>Qu'est-ce qu'un droit d'accès ?</a></li>
      <li><a href="#ajouter"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>Ajouter ou retirer un droit d'accès</a></li>
      <li><a href="#droits"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>Les différents droits d'accès</a></li>
      <li><a href="#suite"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>Aller plus loin</a></li>
    </ol></nav>

    <aside class="who" aria-labelledby="who-h"><h2 id="who-h"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="8" r="3.2"/><path d="M3.5 20c.7-3.6 3-5.3 5.5-5.3s4.8 1.7 5.5 5.3M16 11a3 3 0 1 0 0-6M17.5 14.9c2 .6 3.3 2.2 3.8 5.1"/></svg>Qui peut utiliser cette fonctionnalité ?</h2>
      <div class="who-tags"><span class="wtag">Administrateur du compte</span></div>
      <p>L'administrateur gère les droits d'accès de tous les autres utilisateurs. Les droits disponibles varient selon le forfait : consultez la page <a href="{K}/fr/tarifs-et-fonctionnalites/" target="_blank" rel="noopener">Tarifs et fonctionnalités</a>.</p></aside>

    <section id="definition" class="art-sec"><h2>Qu'est-ce qu'un droit d'accès ?</h2>
      <p>Un droit d'accès est une permission qui détermine ce que chaque utilisateur peut faire ou voir dans votre compte Kiwili. En accordant ou non un droit précis à un utilisateur, vous lui permettez d'accéder à certaines informations ou fonctions du compte.</p>
      <p>Les droits d'accès varient selon votre forfait. Les combinaisons sont nombreuses : vous pouvez associer plusieurs accès pour personnaliser les droits de chaque utilisateur.</p>
      <p class="callout info">Parmi les fonctions de Kiwili, le <a href="{K}/Blog/post/creer-gerer-une-tache-avec-kiwili/" target="_blank" rel="noopener">module tâches</a> est toujours disponible, sauf pour le forfait standard.</p>
    </section>

    <section id="ajouter" class="art-sec"><h2>Comment ajouter ou retirer un droit d'accès ?</h2>
      <p>Pour ajouter ou retirer des accès à un utilisateur :</p>
      <ol class="steps-list"><li><span>Ouvrez la fiche de l'utilisateur.</span></li><li><span>Sous <b>Accès</b>, cochez ou décochez la ou les cases correspondantes.</span></li></ol>
      {fig('ajouter-acces',"Fiche utilisateur : cases à cocher sous Accès, exemple de l'accès projet","Exemple : l'accès projets.")}
    </section>

    <section id="droits" class="art-sec"><h2>Les différents droits d'accès</h2>
      <p>Voici les {total} droits d'accès détaillés dans ce guide, regroupés par domaine. Filtrez la liste ou ouvrez un droit pour voir en détail ce qu'il permet.</p>
      <div class="rtools">
        <div class="rsearch"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg><label class="sr" for="q">Filtrer les droits d'accès</label><input id="q" type="search" placeholder="Filtrer : factures, temps, salaire…" autocomplete="off"></div>
        <button class="expand" id="expand" type="button">Tout déplier</button>
      </div>
      <div class="gchips" role="group" aria-label="Domaines">{chips}</div>
      <p class="rcount" id="rcount" role="status" aria-live="polite">{total} droits affichés</p>
      <div class="rights" id="rights">{rights}</div>
      <p class="rempty" id="rempty" hidden>Aucun droit ne correspond à cette recherche.</p>
    </section>

    <section id="suite" class="art-sec"><h2>Aller plus loin</h2>
      <p>Maintenant que vous connaissez l'essentiel sur les droits d'accès, explorez les différentes combinaisons possibles pour répondre au mieux à vos besoins.</p>
      <div class="more-grid">{morehtml}</div>
      <div class="helpbox"><div><h3>Besoin d'aide ?</h3><p>Vous voulez en savoir plus sur les fonctionnalités de Kiwili ? Lisez notre section aide ou contactez-nous.</p></div><div class="helpbtns"><a class="btn btn-ghost" href="{K}/aide/" target="_blank" rel="noopener">Section aide</a><a class="btn btn-primary" href="{K}/Blog/post/contacter-le-support-de-kiwili/" target="_blank" rel="noopener">Nous contacter</a></div></div>
    </section>

    <section class="feedback" aria-labelledby="fb-h"><h2 id="fb-h">Cet article vous a-t-il été utile ?</h2><div class="fb-btns" id="fb"><button type="button" data-v="yes">Oui</button><button type="button" data-v="no">Non</button></div><p class="fb-done" id="fb-done" hidden></p></section>
   </article>
  </main>
</div>

<section class="tuto-cta on-dark"><div class="container"><div><h2>Essayez Kiwili pendant 14 jours</h2><p>Sans carte de crédit. L'essai inclut l'ensemble des fonctionnalités.</p></div><a class="btn btn-accent" href="https://signup.kiwili.com/signup/?lng=fr" target="_blank" rel="noopener">Commencer</a></div></section>
{footer}
<script src="js/main.js"></script>
<script src="js/tutorial.js"></script>
</body></html>'''
open('tutoriel.html','w').write(page)
print(len(page)//1024,'KB',total,'rights')
