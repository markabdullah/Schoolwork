
import java.util.ArrayList;

public class Genre {
	private String name;
	private ArrayList<Artist> artists;

	Genre(String name) {
		this.name = name;
		this.artists = new ArrayList<>();
	}

	public ArrayList<Artist> getArtists(){
		return this.artists;
	}

	public boolean isPlayedBy(Artist a){
		return a.getGenres().contains(this);
	}

	public boolean hasSameArtist(Genre g){
		for(int i = 0; i < this.artists.size(); i++){
			for(int j = 0; j < g.getArtists().size(); i++){
				Artist a1 = this.artists.get(i);
				Artist a2 = g.getArtists().get(j);
				if(a1.equals(a2)) return true;
			}
		}
		return false;
	}

	public void addArtist(Artist a){
		this.artists.add(a);
		if(!(a.getGenres().contains(this))) a.addGenre(this);
	}

	public boolean equals(Genre g){
		if(!(this.name == g.getName() && this.artists.size() == g.getArtists().size())) return false;
		for(int i = 0; i < this.artists.size(); i++){
			if(!(this.artists.contains(g.getArtists().get(i)))) return false;
		}
		return true;
	}

	public String getName(){
		return this.name;
	}

	public String toString(){
		StringBuilder s = new StringBuilder(this.name + " (");
		for(int i = 0; i < this.artists.size(); i++){
			s.append(this.artists.get(i).getName());
			if(!(i == this.artists.size() - 1)) s.append(", ");
		}
		s.append(")");
		return String.valueOf(s);
	}

}
