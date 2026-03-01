"""
CIS-4930 Introduction to Python, Spring 2026
Homework : 3
Problem : 1
Student Name: Ammiel Bowen
Student ID: ab22dv
Section: 0003
Submission Date: 03-01-2026
"""

# oop heavy one
# movie/customer/vipcustomer/showtime abstract etc etc
from abc import ABC, abstractmethod


# -----------------------------
# Movie class
# -----------------------------
class Movie:
    # store title duration genre.
    def __init__(self, title: str, duration: int, genre: str):
        self.title = title
        self.duration = duration
        self.genre = genre

    @property
    def ticket_price(self):
        # longer movies = 12, shorter = 10
        #using 120 mins as the split (2 hours)
        if self.duration >= 120:
            return 12
        return 10

    def __str__(self):
        # pretty print
        return f"{self.title} ({self.duration} min): {self.genre}"

    def __repr__(self):
        # debug= repr
        return f"Movie(title={self.title!r}, duration={self.duration!r}, genre={self.genre!r})"

# -----------------------------
# Customer class
# -----------------------------
class Customer:
    def __init__(self, name: str, member_id: str, favorite_genre: str = "Any"):
        self.name = name
        self.member_id = member_id
        self.favorite_genre = favorite_genre

        # private points. not used directly
        self._loyalty_points = 0

        # collections
        self.purchased_movies = []   # movies they bought
        self._showtimes_attended = []  # showtimes they went to

    @property
    def loyalty_points(self):
        return self._loyalty_points

    @loyalty_points.setter
    def loyalty_points(self, value):
        # valid 0-10000 
        #keep strict
        if value < 0 or value > 10000:
            raise ValueError("loyalty_points must be within 0-10000")
        self._loyalty_points = value

    def loves_genre(self, genre: str):
        # favorite is "Any" means yes for everything
        # also allow exact match
        if self.favorite_genre == "Any":
            return True
        return self.favorite_genre == genre

    def buy_ticket(self, movie: Movie):
        # collect purchased movies
        self.purchased_movies.append(movie)

    def add_showtime(self, showtime):
        # store showtimes attended (polymorphism )
        self._showtimes_attended.append(showtime)

    def total_revenue(self):
        # total revenue from attended showtimes
        # this works  of Matinee vs EveningPremiere
        total = 0
        for st in self._showtimes_attended:
            total += st.revenue_potential()
        return total

    def __str__(self):
        # "Emma (Action fan, 250 pts)"
        # if Any, still show Any
        return f"{self.name} ({self.favorite_genre} fan, {self.loyalty_points} pts)"

    def __repr__(self):
        return f"Customer(name={self.name!r}, member_id={self.member_id!r}, favorite_genre={self.favorite_genre!r}, points={self.loyalty_points!r})"


# -----------------------------
# VIPCustomer (inheritance)
# -----------------------------
class VIPCustomer(Customer):
    def __init__(self, name: str, member_id: str, vip_tier: str, favorite_genre: str = "Any"):
        #  super() required
        super().__init__(name, member_id, favorite_genre)
        self.vip_tier = vip_tier  # Gold / Platinum / Diamond

    def loves_genre(self, genre: str):
        # VIP auto likes "VIP" genre always
        if genre == "VIP":
            return True
        # otherwise fall back to normal customer logic
        return super().loves_genre(genre)

    def perks(self):
        # perks by tier
        # simple mapping
        if self.vip_tier == "Gold":
            return "Free popcorn"
        elif self.vip_tier == "Platinum":
            return "Free popcorn + drink"
        elif self.vip_tier == "Diamond":
            return "Backstage lounge + free snacks"
        else:
            # if tier unknown just give something generic
            return "VIP perks"

    def __str__(self):
        # custom print format showing VIP status
        return f"{self.name} (VIP {self.vip_tier}, {self.loyalty_points} pts)"


# -----------------------------
# Abstract Showtime + subclasses
# -----------------------------
class Showtime(ABC):
    # abstract base. forces subclasses to implement revenue_potential
    def __init__(self, movie: Movie, tickets_sold: int):
        self.movie = movie
        self.tickets_sold = tickets_sold

    @abstractmethod
    def revenue_potential(self):
        # subclasses must implement
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(movie={self.movie.title!r}, tickets_sold={self.tickets_sold!r})"


class Matinee(Showtime):
    # fixed $8 per ticket
    def revenue_potential(self):
        return self.tickets_sold * 8


class EveningPremiere(Showtime):
    # uses movie.ticket_price ($10 or $12)
    def revenue_potential(self):
        return self.tickets_sold * self.movie.ticket_price


# -----------------------------
# TheaterManager class
# -----------------------------
class TheaterManager:
    def __init__(self):
        # customers by id, movies by title
        self.customers = {}  # id -> Customer
        self.movies = {}     # title -> Movie

    def add_customer(self, customer: Customer):
        self.customers[customer.member_id] = customer

    def add_movie(self, movie: Movie):
        self.movies[movie.title] = movie

    def action_fans(self):
        # list comprehension: all customers who love Action
        return [c.name for c in self.customers.values() if c.loves_genre("Action")]

    def points_map(self):
        # dict comprehension: customer id -> loyalty points
        return {cid: cust.loyalty_points for cid, cust in self.customers.items()}

    def showtimes_for_movie(self, movie_title: str):
        # generator: yield customer names + showtime type for a specific movie
        # format: "Emma-Matinee"
        for cust in self.customers.values():
            # go through  attended showtimes
            for st in cust._showtimes_attended:
                if st.movie.title == movie_title:
                    yield f"{cust.name}-{st.__class__.__name__}"


# -----------------------------
# Demo / main
# -----------------------------
def main():
    # make 2 movies
    avengers = Movie("Avengers", 150, "Action")
    spiderman = Movie("Spider-Man", 110, "VIP")  # making it VIP-ish so Liam auto likes

    # make customers (1 normal, 1 vip)
    emma = Customer("Emma", "M123", "Action")
    emma.loyalty_points = 250  # using property (encapsulation)
    liam = VIPCustomer("Liam", "V456", "Platinum", "Any")
    liam.loyalty_points = 1200

    # showtimes (mix types)
    # these ticket_sold numbers are picked so Emma total revenue for Avengers becomes 890 like sample:
    # Matinee: 100*8=800, EveningPremiere: 9*10=90 => 890
    st1 = Matinee(avengers, 100)
    st2 = EveningPremiere(avengers, 9)

    # spiderman showtime for Liam (evening premiere uses movie ticket_price)
    st3 = EveningPremiere(spiderman, 1)

    # customers buy tickets + attend showtimes
    emma.buy_ticket(avengers)
    emma.add_showtime(st1)
    emma.add_showtime(st2)

    liam.buy_ticket(spiderman)
    liam.add_showtime(st3)

    # manager
    mgr = TheaterManager()
    mgr.add_movie(avengers)
    mgr.add_movie(spiderman)
    mgr.add_customer(emma)
    mgr.add_customer(liam)

    # ---------------------------
    # OOP pillars documentation (required comments)
    # ---------------------------
    # INHERITANCE: VIPCustomer inherits from Customer
    # ENCAPSULATION: loyalty_points is private-ish with validation
    # ABSTRACTION: Showtime is abstract (forces revenue_potential in subclasses)
    # POLYMORPHISM: Customer.total_revenue() calls revenue_potential on Matinee and EveningPremiere same way

    # report printing (like expected)
    print("🎬 Starry Night Cinemas Report")

    # Emma line: "- Emma (Action fan, 250 pts): Avengers ($890 revenue)"
    print(f"- {emma}: {emma.purchased_movies[0].title} (${emma.total_revenue()} revenue)")

    # Liam line: "- Liam (VIP Platinum, 1200 pts): Spider-Man (Free popcorn + drink)"
    print(f"- {liam}: {liam.purchased_movies[0].title} ({liam.perks()})")

    # action fans list
    print("Action fans:", mgr.action_fans())

    #  map dict
    print("Points:", mgr.points_map())

    # generator output for Avengers
    show_list = ", ".join([x for x in mgr.showtimes_for_movie("Avengers")])
    print(f"Showtimes for Avengers: {show_list}")


if __name__ == "__main__":
    main()