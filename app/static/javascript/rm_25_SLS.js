document.addEventListener('DOMContentLoaded', function() {
    const toggleMassCar = document.querySelector('#button-mass-car');
    const splitMassCar = document.querySelector('#split-mass-car');
    const MassCarFrom = document.querySelector('#mass-car-form');

    const toggleMassDriver = document.querySelector('#button-mass-driver');
    const splitMassDriver = document.querySelector('#split-mass-driver');
    const MassDriverFrom = document.querySelector('#mass-driver-form');

    const toggleProportionFront = document.querySelector('#button-proportion-front');
    const splitProportionFront = document.querySelector('#split-proportion-front');
    const ProportionFrontFrom = document.querySelector('#proportion-front-form');

    const toggleFrontTrackWidth = document.querySelector('#button-front-track-width');
    const splitFrontTrackWidth = document.querySelector('#split-front-track-width');
    const FrontTrackWidthFrom = document.querySelector('#front-track-width-form');

    const rearTrackWidth = document.querySelector('#button-rear-track-width');
    const splitRearTrackWidth = document.querySelector('#split-rear-track-width');
    const rearTrackWidthForm = document.querySelector('#rear-track-width-form');

    const toggleWheelbase = document.querySelector('#button-wheelbase');
    const splitWheelbase = document.querySelector('#split-wheelbase');
    const WheelbaseFrom = document.querySelector('#wheelbase-form');

    const toggleCGHeight = document.querySelector('#button-cg-height');
    const splitCGHeight = document.querySelector('#split-cg-height');
    const CGHeightForm = document.querySelector('#cg-height-form');

    const toggleYawInertia = document.querySelector('#button-yaw-inertia');
    const splitYawInertia = document.querySelector('#split-yaw-inertia');
    const yawInertiaForm = document.querySelector('#yaw-inertia-form');

    const toggleCof = document.querySelector('#button-cof');
    const splitCof = document.querySelector('#split-cof');
    const CofForm = document.querySelector('#cof-form');

    const toggleLoadSensitivity = document.querySelector('#button-load-sensitivity');
    const splitLoadSensitivity = document.querySelector('#split-load-sensitivity');
    const loadSensitivityForm = document.querySelector('#load-sensitivity-form');

    const toggleCd = document.querySelector('#button-cd');
    const splitCd = document.querySelector('#split-cd');
    const CdForm = document.querySelector('#cd-form');

    const toggleCl = document.querySelector('#button-cl');
    const splitCl = document.querySelector('#split-cl');
    const ClForm = document.querySelector('#cl-form');

    const toggleA = document.querySelector('#button-a');
    const splitA = document.querySelector('#split-a');
    const AForm = document.querySelector('#a-form');

    const toggleRho = document.querySelector('#button-rho');
    const splitRho = document.querySelector('#split-rho');
    const RhoForm = document.querySelector('#rho-form');

    const toggleFrontDownforce = document.querySelector('#button-front-downforce');
    const splitFrontDownforce = document.querySelector('#split-front-downforce');
    const frontDownforceForm = document.querySelector('#front-downforce-form');

    const toggleCpHeight = document.querySelector('#button-cp-height');
    const splitCpHeight = document.querySelector('#split-cp-height');
    const CpHeightForm = document.querySelector('#cp-height-form');

    const toggleBrakeBias = document.querySelector('#button-brake-bias');
    const splitBrakeBias = document.querySelector('#split-brake-bias');
    const BrakeBiasForm = document.querySelector('#brake-bias-form');

    const togglePrimaryDriver = document.querySelector('#button-primary-drive');
    const splitPrimaryDriver = document.querySelector('#split-primary-drive');
    const PrimaryDriverForm = document.querySelector('#primary-drive-form');

    const toggleEngineSprocketTeeth = document.querySelector('#button-engine-sprocket-teeth');
    const splitEngineSprocketTeeth = document.querySelector('#split-engine-sprocket-teeth');
    const EngineSprocketTeethForm = document.querySelector('#engine-sprocket-teeth-form');

    const toggleDiffSprocketTeeth = document.querySelector('#button-diff-sprocket-teeth');
    const splitDiffSprocketTeeth = document.querySelector('#split-diff-sprocket-teeth');
    const DiffSprocketTeethForm = document.querySelector('#diff-sprocket-teeth-form');

    const toggleTireRadius = document.querySelector('#button-tire-radius');
    const splitTireRadius = document.querySelector('#split-tire-radius');
    const TireRadiusForm = document.querySelector('#tire-radius-form');

    const toggleGearRatios = document.querySelector('#button-gear-ratios');
    const splitGearRatios = document.querySelector('#split-gear-ratios');
    const GearRatiosForm = document.querySelector('#gear-ratios-form');


    toggleMassCar.addEventListener('click', function() {
      if (splitMassCar.style.display === 'none') {
        splitMassCar.style.display = 'block';
        MassCarFrom.style.display = 'none';
      } else {
        splitMassCar.style.display = 'none';
        MassCarFrom.style.display = 'block';
      }
    });

    toggleMassDriver.addEventListener('click', function() {
        if (splitMassDriver.style.display === 'none') {
            splitMassDriver.style.display = 'block';
            MassDriverFrom.style.display = 'none';
        } else {
            splitMassDriver.style.display = 'none';
            MassDriverFrom.style.display = 'block';
        }
    });

    toggleProportionFront.addEventListener('click', function() {
        if (splitProportionFront.style.display === 'none') {
            splitProportionFront.style.display = 'block';
            ProportionFrontFrom.style.display = 'none';
        } else {
            splitProportionFront.style.display = 'none';
            ProportionFrontFrom.style.display = 'block';
        }
    });

    toggleFrontTrackWidth.addEventListener('click', function() {
        if (splitFrontTrackWidth.style.display === 'none') {
            splitFrontTrackWidth.style.display = 'block';
            FrontTrackWidthFrom.style.display = 'none';
        } else {
            splitFrontTrackWidth.style.display = 'none';
            FrontTrackWidthFrom.style.display = 'block';
        }
    });

    rearTrackWidth.addEventListener('click', function() {
        if (splitRearTrackWidth.style.display === 'none') {
            splitRearTrackWidth.style.display = 'block';
            rearTrackWidthForm.style.display = 'none';
        } else {
            splitRearTrackWidth.style.display = 'none';
            rearTrackWidthForm.style.display = 'block';
        }
    });

    toggleWheelbase.addEventListener('click', function() {
        if (splitWheelbase.style.display === 'none') {
            splitWheelbase.style.display = 'block';
            WheelbaseFrom.style.display = 'none';
        } else {
            splitWheelbase.style.display = 'none';
            WheelbaseFrom.style.display = 'block';
        }
    });

    toggleCGHeight.addEventListener('click', function() {
        if (splitCGHeight.style.display === 'none') {
            splitCGHeight.style.display = 'block';
            CGHeightForm.style.display = 'none';
        } else {
            splitCGHeight.style.display = 'none';
            CGHeightForm.style.display = 'block';
        }
    });

    toggleYawInertia.addEventListener('click', function() {
        if (splitYawInertia.style.display === 'none') {
            splitYawInertia.style.display = 'block';
            yawInertiaForm.style.display = 'none';
        } else {
            splitYawInertia.style.display = 'none';
            yawInertiaForm.style.display = 'block';
        }
    });

    toggleCof.addEventListener('click', function() {
        if (splitCof.style.display === 'none') {
            splitCof.style.display = 'block';
            CofForm.style.display = 'none';
        } else {
            splitCof.style.display = 'none';
            CofForm.style.display = 'block';
        }
    });

    toggleLoadSensitivity.addEventListener('click', function() {
        if (splitLoadSensitivity.style.display === 'none') {
            splitLoadSensitivity.style.display = 'block';
            loadSensitivityForm.style.display = 'none';
        } else {
            splitLoadSensitivity.style.display = 'none';
            loadSensitivityForm.style.display = 'block';
        }
    });

    toggleCd.addEventListener('click', function() {
        if (splitCd.style.display === 'none') {
            splitCd.style.display = 'block';
            CdForm.style.display = 'none';
        } else {
            splitCd.style.display = 'none';
            CdForm.style.display = 'block';
        }
    });

    toggleCl.addEventListener('click', function() {
        if (splitCl.style.display === 'none') {
            splitCl.style.display = 'block';
            ClForm.style.display = 'none';
        } else {
            splitCl.style.display = 'none';
            ClForm.style.display = 'block';
        }
    });

    toggleA.addEventListener('click', function() {
        if (splitA.style.display === 'none') {
            splitA.style.display = 'block';
            AForm.style.display = 'none';
        } else {
            splitA.style.display = 'none';
            AForm.style.display = 'block';
        }
    });

    toggleRho.addEventListener('click', function() {
        if (splitRho.style.display === 'none') {
            splitRho.style.display = 'block';
            RhoForm.style.display = 'none';
        } else {
            splitRho.style.display = 'none';
            RhoForm.style.display = 'block';
        }
    });

    toggleFrontDownforce.addEventListener('click', function() {
        if (splitFrontDownforce.style.display === 'none') {
            splitFrontDownforce.style.display = 'block';
            frontDownforceForm.style.display = 'none';
        } else {
            splitFrontDownforce.style.display = 'none';
            frontDownforceForm.style.display = 'block';
        }
    });

    toggleCpHeight.addEventListener('click', function() {
        if (splitCpHeight.style.display === 'none') {
            splitCpHeight.style.display = 'block';
            CpHeightForm.style.display = 'none';
        } else {
            splitCpHeight.style.display = 'none';
            CpHeightForm.style.display = 'block';
        }
    });

    toggleBrakeBias.addEventListener('click', function() {
        if (splitBrakeBias.style.display === 'none') {
            splitBrakeBias.style.display = 'block';
            BrakeBiasForm.style.display = 'none';
        } else {
            splitBrakeBias.style.display = 'none';
            BrakeBiasForm.style.display = 'block';
        }
    });

    togglePrimaryDriver.addEventListener('click', function() {
        if (splitPrimaryDriver.style.display === 'none') {
            splitPrimaryDriver.style.display = 'block';
            PrimaryDriverForm.style.display = 'none';
        } else {
            splitPrimaryDriver.style.display = 'none';
            PrimaryDriverForm.style.display = 'block';
        }
    });

    toggleEngineSprocketTeeth.addEventListener('click', function() {
        if (splitEngineSprocketTeeth.style.display === 'none') {
            splitEngineSprocketTeeth.style.display = 'block';
            EngineSprocketTeethForm.style.display = 'none';
        } else {
            splitEngineSprocketTeeth.style.display = 'none';
            EngineSprocketTeethForm.style.display = 'block';
        }
    });

    toggleDiffSprocketTeeth.addEventListener('click', function() {
        if (splitDiffSprocketTeeth.style.display === 'none') {
            splitDiffSprocketTeeth.style.display = 'block';
            DiffSprocketTeethForm.style.display = 'none';
        } else {
            splitDiffSprocketTeeth.style.display = 'none';
            DiffSprocketTeethForm.style.display = 'block';
        }
    });

    toggleTireRadius.addEventListener('click', function() {
        if (splitTireRadius.style.display === 'none') {
            splitTireRadius.style.display = 'block';
            TireRadiusForm.style.display = 'none';
        } else {
            splitTireRadius.style.display = 'none';
            TireRadiusForm.style.display = 'block';
        }
    });

    toggleGearRatios.addEventListener('click', function() {
        if (splitGearRatios.style.display === 'none') {
            splitGearRatios.style.display = 'block';
            GearRatiosForm.style.display = 'none';
        } else {
            splitGearRatios.style.display = 'none';
            GearRatiosForm.style.display = 'block';
        }
    });
  });