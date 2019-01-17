import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class Playlist {
	private static Map<String, Genre> genres = new HashMap<>();

	public static void main(String[] args) {
		try (BufferedReader reader = new BufferedReader(new FileReader(new File("Music.txt")))) {
				for (String line = reader.readLine(); line != null; line = reader.readLine()) {
					String[] lines = line.split("\\|");
					String name = lines[0].split(",")[0].trim();
					String country = lines[0].split(",")[1].trim();
					Artist a = new Artist(name, country);

				for (int i = 1; i < lines.length; i++) {
					String genre = lines[i].trim();
					if (genres.containsKey(genre)) {
						Genre g = genres.get(genre);
						g.addArtist(a);
					} else {
						Genre g = new Genre(genre);
						genres.put(genre, g);
						g.addArtist(a);
					}
				}
			}
		} catch (IOException e) {
			System.out.println(e.getMessage());
			System.out.println("File I/O error!");
		}


		try (BufferedReader keyboard = new BufferedReader(new InputStreamReader(System.in))) {
			System.out.print("Enter a genre: ");
			String genre = keyboard.readLine();
			while(!genre.equals("exit")){
				if(!(genres.containsKey(genre))){
					System.out.println("This is not a valid genre.");
				}
				else{
					System.out.println(genres.get(genre).toString());
				}
				System.out.print("Enter a genre: ");
				genre = keyboard.readLine();
			}
			System.exit(0);
		}
		catch (IOException e) {
			System.out.println("File I/O error 2!");
		}
	}

}