//
//  ViewController.swift
//  WhatsGood
//
//  Created by Rohit Bandaru on 7/27/17.
//  Copyright © 2017 Rohit Bandaru. All rights reserved.
//

import UIKit
import CoreLocation
import Alamofire
import SwiftyJSON

class ViewController: UIViewController, CLLocationManagerDelegate {

    var locationManager: CLLocationManager = CLLocationManager()
    var currentLocation: CLLocation!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        let label = UILabel(frame: CGRect(x: 0, y: 50, width: 200, height: 30))
        label.center.x = view.center.x
        label.textColor = .black
        label.font = UIFont (name: "Avenir", size: 30)
        label.textAlignment = .center
        label.text = "Whats Good?"
        
        view.addSubview(label)
        
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
        locationManager.delegate = self
        locationManager.requestWhenInUseAuthorization()
        // gets location only one time
        locationManager.startUpdatingLocation()
        currentLocation = nil
        
    }
    
    func locationManager(_ manager: CLLocationManager,
                         didUpdateLocations locations: [CLLocation])
    {
        currentLocation = locations[locations.count - 1]
        print(currentLocation.description)
        locationManager.stopUpdatingLocation()
        
        let latitude:String = "\(currentLocation.coordinate.latitude)"
        let longitude:String = "\(currentLocation.coordinate.longitude)"
        let urlString = "http://127.0.0.1:5000/data/20/"+latitude+"/"+longitude
   
        print(urlString)
        Alamofire.request(urlString).responseJSON { (responseData) -> Void in
            if((responseData.result.value) != nil) {
                let swiftyJsonVar = JSON(responseData.result.value!)
                print(swiftyJsonVar)
            }
        }
    }
    
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

