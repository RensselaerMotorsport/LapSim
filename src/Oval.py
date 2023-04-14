"""A module to simulate Oval"""

from helper_functions_ev import calc_vmax
from helper_functions_ev import forward_int
from helper_functions_ev import braking_length
from helper_functions_ev import straight_line_segment
from classes.car_simple import Car
from random import random
import numpy as np
import math
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
car = Car("data/rm26.json")



#Set Parameters for track
straight_d = 77  #Range 61-77
corner_r = 15    #Range 15-25
n = (straight_d*2)+2  #number of segments

#Track is a two element array that stores the distance of a segment in the first column and its radius in the second
track = np.zeros((n+1,2))

#Create Track Using Parameters
for i in range(n):
    track[i,0] = straight_d/straight_d
#print(track)

#Add Corners for the Oval 
track[straight_d+1,1] = corner_r
track[straight_d+1,0] = 2*math.pi*corner_r
track[(straight_d*2)+1,1] = corner_r
track[(straight_d*2)+1,0] = 2*math.pi*corner_r
track[n,0] = 0
track[n,1] = 0



"""def runtrack(Car, track):
    
    A function to run the oval track given the car object, straight distance, and corner radius and output a time. 
    
    Parameters:
    Car - car object
    track - 2-D array of distance and radius

    Return - Track Time
    
    #Initialize time and velocity arrays, time will be output and velocity can be conditional output (In future)
    time = np.zeros(track.size)
    velocity = np.zeros(track.size)
    velocity[0] = .0001
    
    for i in range(track.size):
        iter = i+1
        if iter == n:
            break

        #print("Iter =",iter)
        #print("Velocity =",velocity[i])
        #print("Radius =",track[i,1])
        #print("Distance=",track[i,0])

        if track[i,1] == 0:
            time[i+1],velocity[i+1] = forward_int(Car, velocity[i],track[i,0], dstep=0.0001)#velocity[i+1] is the exit velocity
            print(velocity)
        else:
            vmax = calc_vmax(corner_r,Car)
            #print("Vmax=", vmax)
            if velocity[i] < vmax or velocity[i] == vmax:
                time[i+1] = (math.pi*corner_r)/velocity[i]
                velocity[i+1] = velocity[i]
            elif velocity > vmax:
                for j in range(1,77):
                    d = braking_length(Car,velocity[-j],vmax,returnVal=1)
                    if d - 77-j < 1:
                        velocity[j:] = braking_length(Car,velocity(-j),vmax,returnVal=2)
                        time[j:] = braking_length(Car,velocity(-j),vmax,returnVal=3)
                time[i+1] = (math.pi*corner_r)/vmax
                velocity[i+1] = vmax



    return ("Lap Time is", np.sum(time, axis=None))"""

#print(runtrack(car, track))


#plt.plot(forward_int(Car, 0,27,returnVal=0),forward_int(Car, 0,27,returnVal=1))
#plt.show
Vsum = 0
Dsum = 0
def run_oval(car, x, r, GR=0, mu=0, dstep=0.01, peak=False):
    """A function for testing the car on an oval track
    
    Given: car, the car object we are considering
    x, the the distance of the straightaway
    r, the radius of the corner
    GR, the gear ratio we are considering
    mu, the friction factor we are considering
    dstep, the distance step we are sweeping over, default is .01 meters
    peak, a boolean representing whether or not we are running at peak torque, default is False and we are not
    
    Returns:
    d, a vector that represents the distance traveled in each step
    v, a vector that represents the car speed in each step"""
    d = [0] # Car distance travelled
    v = [0] # Car speed
    try:
        for i in range(len(x)):
            if r[i] == 0: # Straight segment
                v1 = straight_line_segment(car, v[len(v) - 1], calc_vmax(1 / r[i+1], car), x[i], GR=GR, mu=mu, dstep=dstep, peak=peak)
                for j in range(1, len(v1), 1):
                    v.append(v1[j])
                    d.append(dstep + d[len(d) - 1])
            else: # Cornering
                v1 = min(calc_vmax(1 / r[i], car), v[len(v) - 1])
                global Vsum
                global Dsum
                Vsum += v1 * x[i]
                Dsum += x[i]
                for j in np.arange(0, x[i], dstep):
                    v.append(v1)
                    d.append(dstep + d[len(d) - 1])
    except:
        print("error")
    return d, v

def s_pin(autoX=True):
    if autoX:
        return 10 + random() * 50
    else:
        return 10 + random() * 67

def s_wide(autoX=False):
    if autoX:
        return 10 + random() * 35
    else:
        return 10 + random() * 51

def r_const(autoX=False):
    if autoX:
        return 1 / (23 / 2 + random() * 11)
    else:
        return 1 / (15 + random() * 12)

def r_pin(autoX=False):
    if autoX:
        return 1 / (4.5 + random() * 4.5)
    else:
        return 1 / (4.5 + random() * 4.5)

def construct_track(dist, autoX=True):
    """
    The Autocross course will be designed with the following specifications. Average speeds
    should be 40 km/hr to 48 km/hr
        a. Straights: No longer than 60 m with hairpins at both ends
        b. Straights: No longer than 45 m with wide turns on the ends
        c. Constant Turns: 23 m to 45 m diameter
        d. Hairpin Turns: 9 m minimum outside diameter (of the turn)
        e. Slaloms: Cones in a straight line with 7.62 m to 12.19 m spacing
        f. Miscellaneous: Chicanes, multiple turns, decreasing radius turns, etc.
        g. Minimum track width: 3.5 m
        h. Length of each run should be approximately 0.80 km
    """
    x = []
    r = []
    i = 0
    while sum(x) < dist or i % 2 != 0:
        if i % 2 != 0:
            # Assume turns are between 100 & 170 degree turns
            r.append(r_const(autoX=autoX))
            x.append(2 * math.pi / r[i] * (100 + 70 * random()) / 360)
        else:
            x.append(s_wide(autoX=autoX))
            r.append(0)
        i += 1
    return x, r

default = True
AutoX = False

if default:
    if AutoX:
        x = [11.31777632399167, 41.16297106810914, 37.4418020055827, 32.895684077742246, 19.42579552448383, 40.87478447577049, 38.333286163745456, 44.81636039741031, 10.945553238042002, 43.19453483561845, 10.891957274299646, 46.2028631490988, 17.558594809117324, 27.967050219734332, 30.883611259856174, 21.650643996467327, 10.822423797273402, 34.59755710132988, 43.70527290491272, 32.898235275343545, 31.564542579018607, 32.905526649460384, 41.52151795232453, 36.39265778637454, 26.882344374784562, 53.07895602949566]
        r = [0, 0.06696902368542536, 0, 0.07601419189617506, 0, 0.06439419801517365, 0, 0.04805999460963551, 0, 0.06311484910815798, 0, 0.05647919319181551, 0, 0.07953374084959247, 0, 0.08216431232611547, 0, 0.05120859039882346, 0, 0.0593150624405398, 0, 0.06607891793667274, 0, 0.08064076242366203, 0, 0.04757612698301696]
    else:
        x = [12.972586265471673, 64.10527463155502, 19.78973816992746, 51.90923348523715, 16.334183482148646, 38.848753147924015, 37.0380669225883, 66.04172887615236, 47.50544884332399, 70.2814137833071, 13.117109339005278, 32.93459340515194, 33.274365593477924, 42.258134086767946, 37.93875544154201, 47.35078924234284, 59.866457218488165, 51.240824611964655, 38.23441213277458, 63.9356349141419, 23.367421582082088, 47.445489875450455, 15.036134449295853, 69.30916735215797, 17.304747316226944, 64.99845333971086, 20.098331532727265, 56.94983054184817, 53.36434778405385, 50.547375127184225, 51.26443743639642, 45.41442884331534, 26.825129846613343, 42.7074995101265, 50.722898832664384, 49.59076900090382, 29.295754825814797, 40.23787959660231, 49.33251785828352, 49.44180972800938, 32.46875907506399, 51.76142158067298, 58.1913870745883, 58.571297402530426, 30.350664939586654, 47.99699472020628, 54.90636435844588, 51.54575122530528, 53.904789768700816, 71.95186194728983, 34.88995497323469, 44.04348296640627, 31.476223579857034, 30.999158000852734, 31.232553243919664, 55.76414144057062, 44.3608853708592, 68.20227113361183, 40.58281364303387, 56.90696485949858, 53.09651437093955, 70.63256380979628, 27.80735225553987, 56.079893747111754, 11.98644924168853, 36.31456921563791, 20.875873891142334, 51.81224578539094, 10.24136025703205, 47.920599907000714, 25.542881418542475, 71.51536515811424, 29.053829000414254, 53.20355457554978, 13.448404284305512, 53.83534077872277, 32.28898956994351, 38.90877518517584, 11.169587937345332, 43.28054987129418, 26.171971285103297, 50.571009449001615, 47.9914278227439, 50.66389498215095, 19.200804134095893, 59.607471588518585, 58.01974003169446, 53.63840338945456, 40.190963837771214, 46.386580233269015, 30.51281916539931, 59.742884835723906, 36.263300426462806, 50.109770531270506, 15.32646697914699, 58.6710867679673, 60.91127070563039, 62.107830418101955, 41.033502006721676, 35.51597252262041, 57.40719780909474, 49.20924764832118, 59.453933125080084, 42.90157969547438, 16.65915145000794, 46.85656107969573, 36.22062844233935, 41.26111666145255, 27.088942825468834, 40.96726798024981, 44.73362203920567, 45.38038312996424, 20.14491694465547, 54.2908562977489, 37.9092081831055, 66.07539400689072, 22.207624476152255, 38.83553831956231, 59.83903073124851, 69.92440298647959, 46.74554745094588, 39.48365916936821, 18.088821108952438, 60.10814593942537, 26.443824776313704, 32.33151729822404, 39.511993539932476, 56.26727641005979, 42.26948193640202, 56.503678464833946, 55.97370030797037, 36.22778091337968, 53.26657126105697, 30.35248796285319, 46.729462076103864, 50.046897610904125, 14.805650729498677, 60.880296397992815, 53.11121927656932, 64.57913440548106, 53.48263072167105, 43.673475731451276, 36.75803183623712, 47.3014788226931, 14.998922474050051, 61.5044904123812, 47.44416432808717, 72.65681667458558, 45.41904090168549, 40.14314663984231, 54.019850502715265, 36.453270600800046, 43.533632802791956, 50.18773521462438, 40.30093714607355, 43.49461545180631, 54.08835107040088, 33.243827879582845, 47.905202765119896, 34.092300981346156, 29.838069123745015, 41.82788983619926, 24.968663778730573, 52.07781568796822, 45.38709396539573, 43.0913109667615, 20.480474631225363, 76.58468190959238, 26.40045098169697, 45.39928346479128, 37.88492076810431, 52.30779756301388, 55.190601015912776, 54.43749670907161, 38.637900575489574, 34.21145438354733, 16.668060357616802, 60.54614052563149, 12.719628649857118, 48.05073278676018, 35.03445690606928, 56.08335440655145, 30.697662095781105, 42.707690885543684, 54.80892565443896, 43.69925146740214, 28.386035476628372, 44.10161585463712, 16.335551153535995, 34.58289802858336, 19.63557923327283, 46.71906574179787, 28.146767162983654, 51.82144624133154, 18.928927806343165, 32.86369867595048, 37.09742480860052, 46.46569439155734, 14.822161647998838, 55.74006920092715, 30.66970526392824, 51.4937726569745, 10.001876696999098, 60.30362923927762, 35.58757097139902, 36.88156229202544, 32.14086352931866, 48.55529662178075, 59.74245761716715, 48.56729595835168, 10.529132774032183, 57.48252759241078, 21.60606185701365, 51.73300907346345, 50.5615099194217, 55.71062242092706, 38.70211300267554, 74.38293218453013, 16.455472367371563, 49.57319725416606, 55.1145279501089, 75.2815591379883, 57.34077575378833, 30.027205584922097, 19.005518152838587, 64.01546957901374, 58.82319752285307, 37.13619303656771, 37.209614787744684, 28.60549268474751, 10.22427247756525, 56.01241711254844, 16.500684103730276, 53.7502852239333, 28.012726860724886, 41.00034520780135, 49.92717495200512, 44.497987910018686, 25.78705081560118, 40.97994678454604, 21.33018191699917, 49.94715241849072, 17.770966638486883, 53.75850647669646, 43.67099755801752, 55.586040211726406, 58.613286029807234, 73.14190768229098, 23.888470311172718, 75.14264932032223, 18.393584419689383, 42.383909736374285, 45.73556549588523, 51.85127442825829, 14.821535871465969, 47.97826281903152, 15.62124186451437, 36.16449732246037, 28.746577960129585, 42.58909709753375, 47.58773208514335, 40.82122565957002, 20.709596836854967, 31.54887365989711, 39.764664825187964, 41.69537946801283, 53.4886289121422, 63.07373217456909, 50.92214908078006, 41.91504576214041, 38.17196315810209, 51.95924396219155, 32.62876544031447, 78.07598327668909, 48.097862793257036, 54.8895438954567, 27.798909872186833, 54.36952827010846, 45.2174054989425, 51.630763925630355, 23.810243038603875, 62.11938266418357, 39.51733083563791, 56.96810376726896, 31.634321526445692, 37.216999344510164, 42.849534010646316, 65.79124489518031, 14.248005883952668, 38.58891639410178, 14.079773284321483, 58.972069727118964, 45.10749856336484, 41.04535995603222, 37.38919320669756, 50.889003113531814, 19.037543494980625, 51.57869010054573, 34.43695750604968, 68.60106406157774, 15.773605015531464, 34.39717442442207, 29.955498969929913, 44.3126709517143, 45.38755947331142, 43.974956976245856, 24.06634997130417, 48.10332666684266, 54.88954483414787, 44.31782571221191, 58.271600152235195, 49.52279305243156, 24.257612553476733, 51.98185268405773, 21.01555947153533, 33.04128766375707, 36.61515522252966, 63.54103821777366, 32.216913486005296, 40.6704837942051, 57.39147918303715, 43.75424986689389, 30.496073128013673, 73.53157865818763, 20.148310400481247, 32.59632563903258, 29.164914919533274, 63.36468718106687, 11.986457873276837, 55.41907423827725, 43.19722975893142, 39.092368342801876, 12.701631072034044, 47.75049810184369, 18.469271764152218, 68.67811145005246, 52.83124344697012, 61.374081467124284, 40.5847970866277, 50.49587597334599, 27.095469081125156, 41.04191399801868, 28.672349173753148, 34.51029234064209, 47.570813435165874, 47.51855996354126, 52.37348493453451, 71.53717492029061, 40.48510733891739, 38.59426773440444, 54.95930357127531, 35.160462489694275, 56.48552515705074, 53.508400298954385, 15.742210369115167, 40.27954239299466, 40.38026758382293, 58.556647405464545, 35.38046035814659, 49.4785454457168, 32.434056680977335, 53.733762449200114, 32.75175212374904, 59.3379145130813, 47.467347094238356, 68.1802242905742, 15.026139802515795, 52.23644273675716, 18.797920570905575, 71.90156012864497, 60.845350299691106, 50.53157806770864, 28.671834013291345, 37.29513026813734, 38.36413904770292, 58.09259865988818, 40.46751372206941, 54.68260743185653, 22.913369194898902, 48.055132205274376, 34.48831588521506, 53.766315135036145, 33.00259872365342, 31.408334848478287, 57.589777891731046, 44.368040151711476, 55.90509064727254, 38.63822981434274, 20.0143452074496, 39.623886551670026, 35.08736766436228, 37.12817828586279, 23.686992439184202, 34.65484096059356, 42.70550897558082, 47.95088824888303, 43.42187841454297, 34.47026456077702, 59.13279723042441, 42.241695033564234, 41.60668349718557, 59.255223692359756, 49.39837312871779, 42.44390968330622, 21.6893095122732, 28.56647385624258, 24.976813249675427, 53.24631257154483, 58.90676046677681, 43.518257358695344, 17.738774535320427, 40.44090276444823, 31.331993985824905, 46.062720631797944, 12.88724183947006, 54.560985007556226, 23.609888135167214, 47.911149511429926, 47.859538812912994, 63.95201023790375, 59.39624939681849, 77.98374825023588, 11.043446082135858, 47.576608497913064, 21.82616234650404, 46.389376354594766, 12.967643118739767, 62.176499815908535, 33.65957106474383, 34.96962793644241, 34.592905275836834, 63.28351546216105, 12.305104534656063, 50.974662896304636, 41.89131622244473, 30.77224703702668, 14.956560113368681, 39.05840433329781, 33.85926684154694, 55.26827912116611, 18.25794880808811, 54.301567605461464, 57.94338736636349, 53.07586841790273, 28.558585770301466, 43.64522922878372, 53.116710302150395, 42.16111764031791, 16.708430777982326, 44.92033775943048, 50.28014584891998, 46.782630985387975, 24.052188346926556, 50.07922184020842, 24.60557979765958, 51.65309396982852, 18.503973151322185, 59.4880004492052, 42.29501584687116, 61.893950649663, 35.941972594889464, 60.381844598495405, 41.32201732573246, 72.49807096062953, 54.83158691452688, 45.003641279587164, 17.234625270848426, 67.8277942281451, 27.521351198963824, 63.56636943577997, 15.740511387321956, 44.995491211469954, 54.22414100127593, 47.08191292906931, 10.162176046256855, 36.767637808989186, 45.97949032706995, 48.13748338863644, 50.31496104887016, 46.859952144741854, 38.010829424270966, 53.1483958501076, 14.00562719538506, 46.407150196752625, 21.266209076509984, 62.09554504410248, 57.2353548573659, 48.37531553510421, 31.333515874468713, 45.81410078684688, 33.66119317026242, 39.08822404862899, 22.967588987785216, 46.02794035349253, 33.91470465728685, 45.43973118417291, 54.510906433850316, 41.271392867430556, 28.302595061718765, 34.687537591466786, 19.238634634611827, 44.77152270440227, 39.680975332353135, 39.32890033040381, 24.425971114497685, 44.74013428957389, 25.779934905737377, 49.661056873579, 18.980065722109703, 62.080406163402536, 19.426362220296525, 35.519091849471444, 42.979785405747336, 57.76821101680925, 54.11913621676558, 73.48830998337576, 39.04923683763069, 45.211112236923455, 60.128435526962726, 34.9095502021827, 53.53099206474411, 43.47689539295221]
        r = [0, 0.045566736145216426, 0, 0.050260072435421056, 0, 0.045495983139419445, 0, 0.03735655561061055, 0, 0.041366672043625, 0, 0.05714066347316639, 0, 0.042253393604420326, 0, 0.04734496766463014, 0, 0.04031466681534657, 0, 0.037239818136272695, 0, 0.03877687648993009, 0, 0.03739457274978502, 0, 0.03704442229309874, 0, 0.03962592277867067, 0, 0.056794753638997025, 0, 0.05069631310028609, 0, 0.042193220328066196, 0, 0.05976588929734011, 0, 0.04383883310710149, 0, 0.047492510372706465, 0, 0.03817318602056159, 0, 0.04716133556672297, 0, 0.06056742417992427, 0, 0.05240733471283008, 0, 0.038234036397610575, 0, 0.0493304346211306, 0, 0.06585085656794144, 0, 0.04639995443745504, 0, 0.038144998427566044, 0, 0.04742815355972998, 0, 0.039309126728266426, 0, 0.04188890959948224, 0, 0.04995913424528021, 0, 0.04747762270078997, 0, 0.039573751464643425, 0, 0.04082037983069339, 0, 0.04665209650288631, 0, 0.0513612954108616, 0, 0.05003831656798936, 0, 0.05312290540326123, 0, 0.04660074988973326, 0, 0.05577251798217874, 0, 0.04608052173269898, 0, 0.05014788540718521, 0, 0.05138143858284791, 0, 0.046332162855225276, 0, 0.04256671599908251, 0, 0.04962290829560284, 0, 0.03816266569759586, 0, 0.05761154772015308, 0, 0.05164919375754227, 0, 0.06238559736315903, 0, 0.043171192813578375, 0, 0.06272882961700728, 0, 0.048636953808650595, 0, 0.062028769914047974, 0, 0.04874749205524235, 0, 0.03839785886086225, 0, 0.054200434351258944, 0, 0.04075883603913027, 0, 0.05041565079183348, 0, 0.038659170895545394, 0, 0.06403947737128822, 0, 0.04586126212655049, 0, 0.04932637287343883, 0, 0.06590477717612094, 0, 0.061265856419868224, 0, 0.04452239139435223, 0, 0.04412588675178954, 0, 0.03967968007177551, 0, 0.06237691762373609, 0, 0.04084120281347318, 0, 0.04250736117577178, 0, 0.03714533284675638, 0, 0.06257899794456759, 0, 0.06573624963879941, 0, 0.04809146806121024, 0, 0.04505307345989274, 0, 0.06478813175738703, 0, 0.05878038541934467, 0, 0.05481317730408528, 0, 0.05006419395131556, 0, 0.05794677164720277, 0, 0.038190623988350714, 0, 0.050990135027020524, 0, 0.05604995020079516, 0, 0.04278276171698369, 0, 0.06344350667788909, 0, 0.03793388305946224, 0, 0.05598799427882591, 0, 0.04827311551177115, 0, 0.04362824245996377, 0, 0.0448577725577128, 0, 0.04259070754552859, 0, 0.060373368215166506, 0, 0.05950581436993056, 0, 0.05307203319992925, 0, 0.05970012357663608, 0, 0.03846149580473881, 0, 0.04265772938089997, 0, 0.051212250761313555, 0, 0.044104808790505004, 0, 0.04915583041388614, 0, 0.038323329049924734, 0, 0.06057965350136494, 0, 0.03791827590680904, 0, 0.03999933822585954, 0, 0.04259819517627938, 0, 0.03907161522671417, 0, 0.05949055017352296, 0, 0.03853040037584841, 0, 0.05968238296474192, 0, 0.04160138791137139, 0, 0.06026981719832767, 0, 0.06307444722450031, 0, 0.05178965198184215, 0, 0.04393439547401334, 0, 0.05530117779839609, 0, 0.049298453065690084, 0, 0.04334115512019007, 0, 0.046934510648375234, 0, 0.03847298754206375, 0, 0.04661882138740094, 0, 0.037206123458458494, 0, 0.03819967493018974, 0, 0.06500684684176915, 0, 0.03797781398624469, 0, 0.05418744951169814, 0, 0.06561617316421506, 0, 0.042148411540007924, 0, 0.04416666644245887, 0, 0.05845901403719644, 0, 0.05858082727051119, 0, 0.03799845649635702, 0, 0.056002812263886495, 0, 0.053149118773516586, 0, 0.037241606704790695, 0, 0.05395967008829963, 0, 0.05337792295077331, 0, 0.04234755876688018, 0, 0.04210132896118258, 0, 0.049644505923615856, 0, 0.054643018926104646, 0, 0.04316105583560212, 0, 0.050362949600200796, 0, 0.045353792877025415, 0, 0.06200389662531551, 0, 0.041783065972890054, 0, 0.04878216987560328, 0, 0.04044784103052191, 0, 0.05896293003123528, 0, 0.039620602494624735, 0, 0.062445922499927406, 0, 0.05017785236876161, 0, 0.04647983715704877, 0, 0.04702242886890062, 0, 0.055841194452868045, 0, 0.05467762727013924, 0, 0.03731961071883988, 0, 0.04327632521733957, 0, 0.05468567973611965, 0, 0.038395027260866736, 0, 0.0614713473318808, 0, 0.04256460411260892, 0, 0.04310326489972405, 0, 0.05058874996941942, 0, 0.05928502123687858, 0, 0.040374016896024156, 0, 0.0404043129332838, 0, 0.04879763769643629, 0, 0.04936638921762888, 0, 0.051306296592935716, 0, 0.05946977359991449, 0, 0.040273037065332654, 0, 0.055302891884478456, 0, 0.061261998915353486, 0, 0.04922771921509923, 0, 0.05205148452320029, 0, 0.04450234848613711, 0, 0.04329314246058818, 0, 0.043612299087204424, 0, 0.04545247469064306, 0, 0.039423994580212986, 0, 0.04239556994439081, 0, 0.03986412050000142, 0, 0.04584783177178228, 0, 0.04735812287569091, 0, 0.04367429429392057, 0, 0.04462613110969188, 0, 0.059065842514413006, 0, 0.049193090712496924, 0, 0.061633011136363165, 0, 0.04675843960694763, 0, 0.06203089857565434, 0, 0.06628443321515547, 0, 0.06540841315760344, 0, 0.050964669031894186, 0, 0.06032295866454925, 0, 0.05764697420930657, 0, 0.0421345793249866, 0, 0.04038003860712991, 0, 0.05866826505630336, 0, 0.06537889128000435, 0, 0.05238896360890548, 0, 0.05783229584456416, 0, 0.053468642096563525, 0, 0.06148703809249412, 0, 0.049700036135504666, 0, 0.040402804317340626, 0, 0.04575706003912667, 0, 0.037820177508994225, 0, 0.037699928492170055, 0, 0.044454733644684705, 0, 0.04198173601821841, 0, 0.054253297681193385, 0, 0.04460767200581049, 0, 0.039572458160803424, 0, 0.06361803867026966, 0, 0.0565287088159829, 0, 0.04657817313801308, 0, 0.05375204611315839, 0, 0.051987124450483965, 0, 0.051961266301454014, 0, 0.06347033905517203, 0, 0.0576529234598332, 0, 0.04703748176226537, 0, 0.056641775495297, 0, 0.057201712841264366, 0, 0.0469841009346439, 0, 0.04196268834366138, 0, 0.04179643561032392, 0, 0.03863346452457424, 0, 0.043382531908941535, 0, 0.03780416907450199, 0, 0.039603183742198116, 0, 0.06401832325187992, 0, 0.06263286769778914, 0, 0.06032946485775429, 0, 0.04710328443718878, 0, 0.03743991137145598, 0, 0.04876443489695682, 0, 0.06063762074104338, 0, 0.03911060826643815, 0, 0.052839718863823666, 0, 0.043173257887729605, 0, 0.059467237083028784, 0, 0.05179229666494732, 0, 0.06194020682544029, 0, 0.06193209026230277, 0, 0.05878941705511329, 0, 0.04011877038442468, 0, 0.044893620304730215, 0, 0.049290286344837994, 0, 0.05258748811050074, 0, 0.04749035193366017, 0, 0.05729503161932975, 0, 0.03752726649352961, 0, 0.039676349977302544, 0, 0.04534717967869107, 0, 0.061603356180855495, 0, 0.05730512390368772]
else:
    x, r = construct_track(22000, autoX=False)
    print(x)
    print(r)

from time import perf_counter
def plot_graph(GR):
    t0 = perf_counter()
    d, v = run_oval(car, x, r, GR=GR, peak=True)

    t = 0
    for i in range(1, len(d), 1):
        t += (d[i] - d[i - 1]) / v[i]

    for i in range(len(v)):
        v[i] *= 2.237

    plt.figure(figsize=(64,12))
    plt.grid()
    plt.xlim(0, d[len(d) - 1] * 1.01)
    plt.ylim(0, max(v) * 1.05)

    plt.plot(d, v)
    tav = round(t,3)
    vav = round(d[len(d) - 1] / t * 2.237, 1)
    plt.title(str(tav) + " seconds; " + str(vav) + " mph average")
    plt.suptitle(str(round(GR,2)) + " Gear ratio")
    plt.xlabel("Distance (m)")
    plt.ylabel("Velocity (mph)")
    plt.show()
    t1 = perf_counter()
    return t1 - t0

def plot_GRs(LGR, UGR, count=60):
    T = []
    GR = np.linspace(LGR, UGR, count)
    for i in range(len(GR)):
        t = 0
        d, v = run_oval(car, x, r, GR=GR[i], peak=True)
        for j in range(1, len(d), 1):
            t += (d[j] - d[j - 1]) / v[j]
        T.append(t)

    plt.figure(figsize=(9,6))
    plt.grid()
    plt.xlim(min(GR), max(GR))
    plt.ylim(min(T) / 1.005, max(T) * 1.005)

    plt.plot(GR, T)
    plt.xlabel("Gear ratio")
    plt.ylabel("Autocross time (s)")
    plt.show()
#plot_GRs(2.5, 4, count=25)


#print(round(plot_graph(33/12), 5))
print(round(plot_graph(38/12), 5))
print(Vsum / Dsum)
#print(round(plot_graph(42/12), 5))
#print(round(plot_graph(48/12), 5))
#print(round(plot_graph(52/12), 5))