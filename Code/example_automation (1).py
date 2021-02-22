from mcphysics.experiments import drum
import numpy as np

motors    = None
m2k       = None
soundcard = None

def setup(setup_motors=True, setup_m2k=True, setup_soundcard=True):
    """
    Connects to the specified devices.
    """
    
    global motors, m2k, soundcard
    
    # Create the motors instance
    if setup_motors: motors = drum.motors_api('COM7', 'circle')
    
    # Create the soundcard instance
    if setup_soundcard: soundcard = drum.soundcard()
    
    # Create the adalm2000 (m2k) instance and connect.
    if setup_m2k: 
        m2k = drum.adalm2000()
        m2k.button_connect(True)
    
def acquire_m2k():
    """
    Clicks the button to acquire, and waits until it's done.
    Sets Iterations=1 so it doesn't collect data forever!
    
    Returns the plotter shown in the AI Raw Voltages tab.
    """
    # Prevent it from looping.
    m2k.tab_ai.settings['Iterations'] = 1
    
    # Push the button.
    m2k.tab_ai.button_acquire(True)

    # Wait for the button to finish (without freezing everything)
    while m2k.tab_ai.button_acquire(): m2k.window.sleep()
    
    # Return the plot.
    return m2k.tab_ai.plot_raw

def acquire_soundcard():
    """
    Acquires a single-shot from the sound card.
    It needs to be configured as you like.
    
    Returns the databox plotter showing the data.
    """
    # Set the iterations to 1
    soundcard.tab_in.settings['Iterations'] = 1
    
    # Push the record button
    soundcard.button_record(True)
    
    # Wait.
    while soundcard.button_record(): soundcard.window.sleep()
    
    # Return the databox
    return soundcard.tab_in.plot_raw

def get_sweep():
    """
    Acquires the quadrature data of a frequency sweep from the sound card.
    The sweep needs to be configure as you like in the soundcard interface.and

    Returns the databox plotter showing the raw quadrature data.
    """
    soundcard.quadratures.button_sweep(True)
    while soundcard.quadratures.button_sweep(): soundcard.window.sleep()

    return soundcard.quadratures.plot_quadratures


def get_dc_vs_angle(r=60, a1=0, a2=355, steps=71, settle=0.5):
    """
    Steps out the angle and collects the mean DC voltage from the ADALM. 
    Returns the list of values.
    
    Parameters
    ----------
    a1, a2 : float
        Starting and stopping angles (degrees)
    steps : int
        How many angles in between.
    settle : float
        Number of seconds to wait before acquiring the DC value.
        
    Returns
    -------
    list of actual angles and averages.
    """
    # Will hold the actual angles and DC voltages
    angles = []
    values = []

    # Loop over all the angles we desire
    for a in np.linspace(a1, a2, steps):
        print('Driving to', r, a)
        r_actual, a_actual = motors.set_ra(r, a)
        m2k.window.sleep(settle)
        d = acquire_m2k()
        
        # Append
        angles.append(a_actual)
        values.append(np.average(d['V1']))

    return angles, values

def square_scan(diag=60, pts=5):
    """
    Scans over a square with a given diagonal lenght, with a given number of
    points along each dimension.

    This function will sort the calculated scan positions by radius to speed
    up the acquisition, and the returned points will include the actual position
    for each measurement, but need to be resorted into whatever order you want.

    Take care to not use too many points, as it will take a really long
    time to perform the scan.

    Parameters
    ----------
    diag : int, optional
        The diagonal length of the square to scan over in mm, by default 60
    pts : int, optional
        The number of points along each axis to scan over, by default 5

    Returns
    -------
    numpy-array, (3,pts*pts), [[float, float]]
        The first column is the real x position, second the real y position.
    """
    maxpos = diag/np.sqrt(2) # Max position along a given axis
    poss = np.linspace(-maxpos,maxpos, pts) # The points along a given axis
    carts = [(x,y) for x in poss for y in poss] # The list of cartesian points
    polars = [motors.get_ra(*cart) for cart in carts] # Convert to polar coords
    polars.sort(key = lambda x: x[0]) # Sort points by first coordinate - radius
    
    x = np.zeros(pts*pts) # To hold the real x positions
    y = np.zeros(pts*pts) # To hold the real y positions

    # Looping over points
    for i,point in enumerate(polars):
        # Set the motor to the given polar coordinate, 
        # and get the real x,y values.
        pos = motors.get_xy(*motors.set_ra(*point))
        # Save the real position
        x[i] = pos[0]
        y[i] = pos[1]
    return np.array([x,y])

if __name__ == "__main__":
    setup()
        

