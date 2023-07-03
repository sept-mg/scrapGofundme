<?php
$db = new SQLite3('donations.db');
$results = $db->query('SELECT * FROM donations');
while ($row = $results->fetchArray(SQLITE3_BOTH)) {
	echo '<li>';
	echo $row["name"];
	echo ' ';
	echo $row["amount"];
	echo ' ';
	echo $row["donation_id"];
	echo ' ';
	echo $row["created_at"];
	echo '</li>';
	echo '</br>';
}
$db->close();
?>