# recommender/recommend.py
import threading
from functools import lru_cache
from geopy.geocoders import Nominatim
from university.models import University, Program
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

geolocator = Nominatim(user_agent="uniApp")
geolock = threading.Lock()

@lru_cache(maxsize=1000)
def geocode_location(location_str):
    with geolock:
        return geolocator.geocode(location_str)

def recommend_universities(mode, academic_interests=None, preferred_location=None, max_results=10):
    """
    Recommend universities based on academic interests or preferred location.

    :param mode: 'academic' or 'location'
    :param academic_interests: List of desired program categories (required if mode is 'academic')
    :param preferred_location: String representing the student's preferred city or area (required if mode is 'location')
    :param max_results: Maximum number of recommendations to return
    :return: List of recommended University instances
    """
    if mode not in ['academic', 'location']:
        raise ValueError("Mode must be either 'academic' or 'location'.")

    if mode == 'academic':
        if not academic_interests:
            raise ValueError("Academic interests must be provided for academic-based recommendations.")
        
        # Filter universities offering the desired programs
        universities = University.objects.filter(
            programs_offered__category__in=academic_interests
        ).distinct()

        # Scoring based on program match
        recommendations = []
        for uni in universities:
            program_matches = uni.programs_offered.filter(category__in=academic_interests).count()
            score = program_matches  
            recommendations.append((uni, score))
        
        recommendations.sort(key=lambda x: x[1], reverse=True)

        recommended_universities = [uni for uni, score in recommendations[:max_results]]
        return recommended_universities

    elif mode == 'location':
        if not preferred_location:
            raise ValueError("Preferred location must be provided for location-based recommendations.")
        
        location = geocode_location(preferred_location)

        if not location:
            raise ValueError("Preferred location not found. Please enter a valid city or area.")

        student_point = Point(location.longitude, location.latitude, srid=4326)

        # Annotate universities with distance from preferred location
        universities = University.objects.annotate(
            distance=Distance('location_point', student_point)
        ).order_by('distance')

        # Scoring based on distance
        recommendations = []
        for uni in universities:
            distance_km = uni.distance.km
            distance_score = 1 / (distance_km + 1)  
            recommendations.append((uni, distance_score))
        
        recommendations.sort(key=lambda x: x[1], reverse=True)

        recommended_universities = [uni for uni, score in recommendations[:max_results]]
        return recommended_universities