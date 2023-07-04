<?php

if (isset($_GET['page'])) {
    // Vérifiez si 'page' est un entier valide entre 1 et 1000
    $nbpage = filter_var($_GET['page'], FILTER_VALIDATE_INT, array(
        'options' => array(
            'min_range' => 1,
            'max_range' => 10
        )
    ));

    if ($nbpage !== false) {

        $db = new SQLite3('donations.db');

        // Définir la limite de résultats par page
        $limit_per_page = 1000;

        $offset = ($nbpage - 1) * $limit_per_page;

        // Utilisation de requête préparée pour éviter les injections SQL
        $query = $db->prepare('SELECT * FROM donations ORDER BY donation_id LIMIT :limit OFFSET :offset');
        $query->bindValue(':limit', $limit_per_page, SQLITE3_INTEGER);
        $query->bindValue(':offset', $offset, SQLITE3_INTEGER);
        $results = $query->execute();
    } else {
        // La valeur de 'page' n'est pas un entier valide entre 1 et 1000
        header("Location: /?page=1");
        exit;
    }
} else {
    // La variable 'page' n'est pas présente dans l'URL
    header("Location: /?page=1");
    exit;
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>laliste des racelars</title>
</head>
<body>
<table>
        <tr>
            <th>Name</th>
            <th>Amount</th>
            <th>Donation-ID</th>
            <th>Created-At-(GMT-5)</th>
        </tr>
        <?php while ($row = $results->fetchArray(SQLITE3_BOTH)) { ?>
            <tr>
                <td><?php echo $row["name"]; ?></td>
                <td><?php echo $row["amount"]; ?> €</td>
                <td><?php echo $row["donation_id"]; ?></td>
                <td><?php echo $row["created_at"]; ?></td>
            </tr>
        <?php } $db->close();?>
    </table>
</body>
</html>