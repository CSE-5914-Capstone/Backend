def scale_tempo(target_value, user_input):
    min_tempo = 0.0
    max_tempo = 239.44000244140625
    range_diff = max_tempo - min_tempo
    scaled_max = min(max_tempo, target_value + (user_input / 10) * range_diff)
    scaled_min = max(min_tempo, target_value - (user_input / 10) * range_diff)
    return scaled_max, scaled_min

def scale_danceability(target_value, user_input):
    min_danceability = 0.0
    max_danceability = 0.9829999804496765
    range_diff = max_danceability - min_danceability
    scaled_max = min(max_danceability, target_value + (user_input / 10) * range_diff)
    scaled_min = max(min_danceability, target_value - (user_input / 10) * range_diff)
    return scaled_max, scaled_min

def scale_energy(target_value, user_input):
    min_energy = 0.00017499999376013875
    max_energy = 1.0
    range_diff = max_energy - min_energy
    scaled_max = min(max_energy, target_value + (user_input / 10) * range_diff)
    scaled_min = max(min_energy, target_value - (user_input / 10) * range_diff)
    return scaled_max, scaled_min

def scale_loudness(target_value, user_input):
    min_loudness = -46.448001861572266
    max_loudness = 1.274999976158142
    range_diff = max_loudness - min_loudness
    scaled_max = min(max_loudness, target_value + (user_input / 10) * range_diff)
    scaled_min = max(min_loudness, target_value - (user_input / 10) * range_diff)
    return scaled_max, scaled_min

def scale_liveness(target_value, user_input):
    min_liveness = 0.0
    max_liveness = 0.9959999918937683
    range_diff = max_liveness - min_liveness
    scaled_max = min(max_liveness, target_value + (user_input / 10) * range_diff)
    scaled_min = max(min_liveness, target_value - (user_input / 10) * range_diff)
    return scaled_max, scaled_min

def scale_valence(target_value, user_input):
    min_valence = 0.0
    max_valence = 0.9909999966621399
    range_diff = max_valence - min_valence
    scaled_max = min(max_valence, target_value + (user_input / 10) * range_diff)
    scaled_min = max(min_valence, target_value - (user_input / 10) * range_diff)
    return scaled_max, scaled_min
