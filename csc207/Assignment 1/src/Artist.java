
import java.util.ArrayList;

public class Artist {
	private String name;
	private ArrayList<Genre> genres;
	private String country;

	Artist(String name, String country) {
		this.name = name;
		this.country = country;
		this.genres = new ArrayList<>();
	}

	public void addGenre(Genre g){
		this.genres.add(g);
		if(!(g.getArtists().contains(this))) g.addArtist(this);
	}

	public boolean equals(Artist a){
		return (this.name == a.name && this.country == a.country);
	}

	public ArrayList<Genre> getGenres(){
		return this.genres;
	}

	public String getName(){
		return this.name;
	}

	public String getCountry(){
		return this.country;
	}

	public String toString(){
		StringBuilder s = new StringBuilder(this.name + ", " + this.country);
		for(int i = 0; i < this.genres.size(); i++){
			s.append(System.lineSeparator() + this.genres.get(i).getName());
		}
		return String.valueOf(s);
	}
}
